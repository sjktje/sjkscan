# -*- coding: utf-8 -*-
"""
    sjkscan.scan
    ~~~~~~~~~~~~

    This module provides scanning functionality.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""

import logging
import os

from datetime import datetime
from .config import config, load_config
from .utils import run_cmd
from .logger import init_logging


def run_scan(output_directory):
    """Run scanimage in batch mode.

    :param string output_directory: directory to write scanned images to

    """
    logging.info('Scanning to %s', output_directory)

    command = [
        'scanimage',
        '--resolution {}'.format(config['Scanimage']['resolution']),
        '--batch={}/scan_%03d.pnm'.format(output_directory),
        '--format=pnm',
        '--mode Gray',
        '--brightness {}'.format(config['Scanimage']['brightness']),
        '--contrast {}'.format(config['Scanimage']['contrast']),
        '--source "ADF Duplex"',
        '-v'
    ]

    run_cmd(command)

    logging.info('Finished scanning to %s', output_directory)


def main():
    """
    Scan documents.

    Documents are placed in data_dir/YYYY-MM-DD_HH-MM-SS.unfinished.
    Once the scan has been completed, the '.unfinished' is removed.

    """

    load_config()
    init_logging(config['Logging']['level'])

    timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    unfinished = os.path.join(config['Paths']['data'], timestamp + '.unfinished')
    finished = os.path.join(config['Paths']['data'], timestamp)
    output_dir = os.path.join(config['Paths']['data'], unfinished)

    logging.debug('Creating output directory %s', output_dir)
    try:
        os.mkdir(output_dir)
    except OSError as e:
        logging.error('Could not create %s: %s', output_dir, e)

    run_scan(output_dir)

    logging.debug('Renaming %s to %s', unfinished, finished)
    try:
        os.rename(unfinished, finished)
    except OSError as e:
        logging.error('Could not rename %s to %s: %s', unfinished, finished, e)
