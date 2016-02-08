#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess

from wand.image import Image


def run_cmd(args):
    """Run shell command and return its output."""

    if isinstance(args, list):
        args = ' '.join(args)

    print("Running: {}".format(args))

    try:
        result = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


def scan(output_directory):
    """Run scanimage in batch mode."""

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
    """Rotate filename given amount of degrees."""
    with Image(filename=filename) as image:
        with image.clone() as rotated:
            rotated.rotate(degrees)
            rotated.save(filename=filename)


def rotate_all_images_in_dir(dirname, degrees):
    """Rotate all files in directory."""
    for f in os.scandir(dirname):
        if not f.is_file():
            next
        rotate_image(os.path.join(dirname, f.name), degrees)


def is_blank(filename):
    """
    Return true if filename is a blank image. This is a slightly modified
    version of Vinatha Ekanayake's is_blank(), which is part of Scanpdf
    (https://github.com/virantha/scanpdf) and licensed under the Apache
    license.

    Returns true if image in filename is blank
    standard deviation: 56.9662 (0.223397)
    """
    if not os.path.exists(filename):
        return True

    c = 'identify -verbose %s' % filename
    result = run_cmd(c)
    mStdDev = re.compile(b'\s*standard deviation:\s*\d+\.\d+\s*\((?P<percent>\d+\.\d+)\).*')

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
    """
    if is_blank(filename):
        print('Removing (probably) blank page {}'.format(filename))
        os.remove(filename)


def main():
    """TODO: docstring"""
    output_dir = 'output'
    scan(output_dir)

    for f in os.scandir(output_dir):
        if not f.is_file():
            next
        remove_if_blank(os.path.join(output_dir, f.name))


    rotate_all_images_in_dir(output_dir, 180)


if __name__ == '__main__':
    main()
