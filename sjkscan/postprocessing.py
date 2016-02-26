# -*- coding: utf-8 -*-
"""
    sjkscan.postprocessing
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements all post processing related actions that sjkscan take on a
    scanned document.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""

import logging
import os
import re
import time

from PyPDF2 import PdfFileMerger
from wand.image import Image

from .config import config, load_config
from .logging import init_logging
from .utils import run_cmd, files, move, remove, is_scan_name, parse_args


def rotate_image(filename, degrees):
    """Rotate image given amount of degrees.

    :param string filename: file to rotate
    :param int degrees: amount of degrees to rotate

    """
    logging.info('Rotating %s %s degrees', filename, degrees)
    with Image(filename=filename) as image:
        with image.clone() as rotated:
            rotated.rotate(degrees)
            rotated.save(filename=filename)


def rotate_all_images_in_dir(dirname, degrees):
    """Rotate all files in directory.

    :param string dirname: name of directory in which files should be rotated
    :param int degrees: number of degrees to rotate

    """
    logging.info('Rotating images %s degrees in directory %s', dirname, degrees)
    for f in files(dirname):
        rotate_image(os.path.join(dirname, f), degrees)


def unpaper(filename):
    """Process file with unpaper and delete original.

    :param filename: file to run unpaper on

    """
    logging.info('Running unpaper on %s', filename)
    unpapered_filename = filename + '.unpapered'
    # TODO: We don't use unpaper's --overwrite because it currently seems to be
    # broken. Once it's been fixed, just --overwrite the original.
    run_cmd('unpaper --size a4 "{}" "{}"'.format(filename, unpapered_filename))
    move(unpapered_filename, filename)


def unpaper_dir(directory, extension=None):
    """Run unpaper on all files with given extension in directory

    :param string directory: directory to process
    :param string extension: extension of files to run unpaper on

    """
    for f in files(directory, extension):
        unpaper(os.path.join(directory, f))


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
        logging.debug('is_blank: file %s does not exist.')
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
                logging.debug('is_blank: %s is NOT blank - standard deviation > 0.05 (%d)', filename, stdev)
                return False

    logging.debug('is_blank: %s is probably blank', filename)
    return True


def move_blanks(input_dir, output_dir):
    """Move blank .pnm's in input_dir to output_dir

    :param string input_dir: directory to check for blank .pnm files
    :param string output_dir: where to move blank .pnm files
    :returns: number of blank pages moved
    :rtype: int

    """
    number_of_blanks = 0

    for file in files(input_dir, 'pnm'):
        image = os.path.join(input_dir, file)

        if is_blank(image):
            try:
                os.mkdir(output_dir)
            except:
                pass  # Assume directory exists.

            move(image, output_dir)
            number_of_blanks += 1

    return number_of_blanks


def remove_if_blank(filename):
    """Remove file if it is blank.

    This is useful when scanning in duplex mode using a backend that doesn't
    support skipping blank pages.

    :param string filename: name of file to remove, if blank

    """
    if is_blank(filename):
        remove(filename)


def merge_pdfs(inputs, output):
    """Merge selected pdfs.

    :param list inputs: files to concatenate
    :param string output: name of file to write

    """
    merger = PdfFileMerger()
    input_fds = dict()

    out = open(output, 'wb')

    logging.info('Merging PDF files into %s...', output)

    for filename in inputs:
        logging.debug('Merging %s -> %s', filename, output)
        try:
            input_fds[filename] = open(filename, 'rb')
        except OSError as e:
            logging.error('Could not open %s: %s', filename, e)
        merger.append(input_fds[filename])

    merger.write(out)
    logging.info('Finished merging PDF files into %s', output)


def merge_pdfs_in_dir(directory, output):
    """Read all pdf files in directory and create one merged output.

    :param string directory: directory containing pdf files to be merged
    :param string output: filename of new merged pdf
    """
    files_to_merge = []

    for pdf in files(directory, 'pdf'):
        files_to_merge.append(os.path.join(directory, pdf))

    merge_pdfs(files_to_merge, output)


def ocr(filename, language):
    """Perform OCR on file using Tesseract.

    :param string filename: file to perform OCR on
    :param string language: language(s) expected to be used in file

    """
    logging.info('Performing OCR (%s) on %s', language, filename)
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
    for file in files(directory, 'pnm'):
        ocr(os.path.join(directory, file), language)


def main(argv=None):
    """
    Polls DATA_DIR for finished scans. Once found, scand will:

        - Move blank images to subdir blank/
        - Rotate remaining images
        - OCR remaining images
        - Merge resulting pdf files
        - Move the directory to INBOX

    """

    load_config()
    init_logging(config['Logging']['level'])

    args = parse_args(argv)

    while True:
        for entry in os.scandir(config['Paths']['data']):
            if not entry.is_dir() or not is_scan_name(entry.name):
                continue

            archive_dir = config['Paths']['archive']
            inbox_dir = config['Paths']['inbox']
            scan_dir = os.path.join(config['Paths']['data'], entry.name)
            pdf_output = os.path.join(inbox_dir, '{}.pdf'.format(entry.name))
            blank_dir = os.path.join(scan_dir, 'blank')

            move_blanks(scan_dir, blank_dir)

            rotate_all_images_in_dir(scan_dir, 180)
            unpaper_dir(scan_dir, 'pnm')
            ocr_pnms_in_dir(scan_dir, 'swe')

            try:
                os.mkdir(archive_dir)
                os.mkdir(inbox_dir)
            except:
                pass  # Assume directories exists.

            merge_pdfs_in_dir(scan_dir, pdf_output)
            move(scan_dir, archive_dir)

        time.sleep(1)
