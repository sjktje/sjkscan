#!/usr/bin/env python
# encoding: utf-8

from wand.image import Image

def run_cmd(args):
    """Run shell command."""
    subprocess.run(args, stderr=subprocess.STDOUT)


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


def page_is_empty(filename):
    """Check if page is empty.

    Return true if it is, otherwise false.
    """
    pass


def main():
    """TODO: docstring"""
    rotate_image('test.pdf', 180)


if __name__ == '__main__':
    main()
