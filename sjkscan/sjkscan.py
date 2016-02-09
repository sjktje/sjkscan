#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess

from wand.image import Image
from PyPDF2 import PdfFileMerger


def run_cmd(args):
    """Run shell command and return its output.

    :param args: list or string of shell command and arguments
    :returns: output of command
    """

    if isinstance(args, list):
        args = ' '.join(args)

    print("Running: {}".format(args))

    try:
        result = subprocess.check_output(
            args,
            stderr=subprocess.STDOUT,
            shell=True)
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


def scan(output_directory):
    """Run scanimage in batch mode.

    :param string output_directory: directory to write scanned images to
    """

    command = [
        'scanimage',
        '--resolution 300',
        '--batch={}/scan_%03d.pnm'.format(output_directory),
        '--format=pnm',
        '--mode Gray',
        '--brightness 80',
        '--contrast 100',
        '--source "ADF Duplex"',
        '-v'
    ]

    run_cmd(command)


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
            next
        rotate_image(os.path.join(dirname, f.name), degrees)


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

    for filename in inputs:
        input_fds[filename] = open(filename, 'rb')
        merger.append(input_fds[filename])

    with open(output, 'wb') as f:
        merger.write(f)


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
