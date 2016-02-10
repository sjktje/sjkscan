#!/usr/bin/env python
# encoding: utf-8

import os
from datetime import datetime
from . import utils


def run_scan(output_directory):
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


def scan():
    """
    Scan documents.

    Documents are placed in data_dir/YYYY-MM-DD_HH-MM-SS.unfinished.
    Once the scan has been completed, the '.unfinished' is removed.

    """
    config = {
        'data_dir': '/Users/sjk/Code/sjkscan/data'
    }

    timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    unfinished = os.path.join(config['data_dir'], timestamp + '.unfinished')
    finished = os.path.join(config['data_dir'], timestamp)
    output_dir = os.path.join(config['data_dir'], unfinished)

    try:
        os.mkdir(output_dir)
    except OSError as e:
        print('Could not create {}: {}', output_dir, e)

    run_scan(output_dir)

    try:
        os.rename(unfinished, finished)
    except OSError as e:
        print('Could not rename {} to {}: {}', unfinished, finished, e)
