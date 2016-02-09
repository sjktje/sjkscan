#!/usr/bin/env python
# encoding: utf-8

from . import utils


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

    utils.run_cmd(command)
