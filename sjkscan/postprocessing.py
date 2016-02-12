import os
import re
import shutil
import time

from .config import config, load_config
from .utils import run_cmd
from PyPDF2 import PdfFileMerger
from wand.image import Image


def rotate_image(filename, degrees):
    """Rotate image given amount of degrees.

    :param string filename: file to rotate
    :param int degrees: amount of degrees to rotate

    """
    with Image(filename=filename) as image:
        with image.clone() as rotated:
            rotated.rotate(degrees)
            rotated.save(filename=filename)


def rotate_all_images_in_dir(dirname, degrees):
    """Rotate all files in directory.

    :param string dirname: name of directory in which files should be rotated
    :param int degrees: number of degrees to rotate

    """
    for f in os.scandir(dirname):
        if not f.is_file():
            continue
        rotate_image(os.path.join(dirname, f.name), degrees)


def unpaper(filename):
    """Process file with unpaper and delete original.

    :param filename: TODO

    """
    unpapered_filename = filename + '.unpapered'
    # TODO: We don't use unpaper's --overwrite because it currently seems to be
    # broken. Once it's been fixed, just --overwrite the original.
    run_cmd('unpaper --size a4 "{}" "{}"'.format(filename, unpapered_filename))
    shutil.move(unpapered_filename, filename)


def unpaper_dir(directory, extension=None):
    """Run unpaper on all files with given extension in directory

    :param string directory: directory to process
    :param string extension: extension of files to run unpaper on

    """

    for f in os.scandir(directory):
        if not f.is_file():
            continue
        if extension and not f.name.endswith('.' + extension):
            continue

        unpaper(os.path.join(directory, f.name))


def is_blank(filename):
    """
    Check if image is blank.

    Return true if filename is a blank image. This is a slightly modified
    version of Vinatha Ekanayake's is_blank(), which is part of Scanpdf
    (https://github.com/virantha/scanpdf) and licensed under the Apache
    license.

    :param string filename: file name of image to check
    :returns: True if image is blank, False otherwise.

    """
    if not os.path.exists(filename):
        return True

    c = 'identify -verbose %s' % filename
    result = run_cmd(c)
    mStdDev = re.compile(
        b'\s*standard deviation:\s*\d+\.\d+\s*\((?P<percent>\d+\.\d+)\).*')

    for line in result.splitlines():
        match = mStdDev.search(line)
        if match:
            stdev = float(match.group('percent'))
            if stdev > 0.05:
                return False

    return True


def move_blanks(input_dir, output_dir):
    """Move blank .pnm's in input_dir to output_dir

    :param string input_dir: directory to check for blank .pnm files
    :param string output_dir: where to move blank .pnm files
    :returns: number of blank pages moved
    :rtype: int

    """
    number_of_blanks = 0

    for entry in os.scandir(input_dir):
        if not entry.is_file() or not entry.name.endswith('.pnm'):
            continue

        image = os.path.join(input_dir, entry.name)

        if is_blank(image):
            try:
                os.mkdir(output_dir)
            except:
                pass  # Assume directory exists.

            shutil.move(image, output_dir)
            number_of_blanks += 1

    return number_of_blanks


def remove_if_blank(filename):
    """Remove file if it is blank.

    This is useful when scanning in duplex mode using a backend that doesn't
    support skipping blank pages.

    :param string filename: name of file to remove, if blank

    """
    if is_blank(filename):
        print('Removing (probably) blank page {}'.format(filename))
        os.remove(filename)


def merge_pdfs(inputs, output):
    """Merge selected pdfs.

    :param list inputs: files to concatenate
    :param string output: name of file to write

    """
    merger = PdfFileMerger()
    input_fds = dict()

    out = open(output, 'wb')

    for filename in inputs:
        try:
            input_fds[filename] = open(filename, 'rb')
        except OSError as e:
            print('Error opening {}: {}'.format(filename, e))
        merger.append(input_fds[filename])

    merger.write(out)


def merge_pdfs_in_dir(directory, output):
    """Read all pdf files in directory and create one merged output.

    :param string directory: directory containing pdf files to be merged
    :param string output: filename of new merged pdf
    """
    files_to_merge = []

    for file in os.scandir(directory):
        if not file.is_file():
            continue
        if file.name[-4:] != '.pdf':
            continue

        files_to_merge.append(os.path.join(directory, file.name))

    merge_pdfs(files_to_merge, output)


def ocr(filename, language):
    """Perform OCR on file using Tesseract.

    :param string filename: file to perform OCR on
    :param string language: language(s) expected to be used in file

    """
    base_output_name = filename[:-4]
    command = 'tesseract {} {} -l {} pdf'.format(filename,
                                                 base_output_name,
                                                 language)
    run_cmd(command)


def ocr_pnms_in_dir(directory, language):
    """Perform OCR on all pnm files in given directory.

    :param string directory: directory in which all pnm files will be OCR:ed
    :param string language: language(s) expected to be used in files

    """
    for file in os.scandir(directory):
        if not file.is_file():
            continue
        if file.name[-4:] != '.pnm':
            continue
        ocr(os.path.join(directory, file.name), language)


def scand():
    """
    Polls DATA_DIR for finished scans. Once found, scand will:

        - Move blank images to subdir blank/
        - Rotate remaining images
        - OCR remaining images
        - Merge resulting pdf files
        - Move the directory to INBOX

    """

    load_config()

    while True:
        for entry in os.scandir(config['Paths']['data']):
            if entry.name.endswith('.unfinished') or not entry.is_dir() or entry.name == 'INBOX':
                continue

            scan_dir = os.path.join(config['Paths']['data'], entry.name)

            move_blanks(scan_dir, os.path.join(scan_dir, 'blank'))

            rotate_all_images_in_dir(scan_dir, 180)

            unpaper_dir(scan_dir, 'pnm')

            ocr_pnms_in_dir(scan_dir, 'swe')

            pdf_output = os.path.join(scan_dir, 'output.pdf')
            merge_pdfs_in_dir(scan_dir, pdf_output)

            inbox_dir = os.path.join(config['Paths']['data'], 'INBOX')

            try:
                os.mkdir(inbox_dir)
            except:
                pass  # Assume directory exists.

            shutil.move(scan_dir, inbox_dir)

        time.sleep(1)
