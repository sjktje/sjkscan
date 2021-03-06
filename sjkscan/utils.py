# -*- coding: utf-8 -*-
"""
    sjkscan.utils
    ~~~~~~~~~~~~~

    This module provides utility functions.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""

import argparse
import datetime
import logging
import os
import shutil
import subprocess

from .config import config
from . import __version__


def run_cmd(args):
    """Run shell command and return its output.

    Arguments and output is logged if log level DEBUG is set. Example usage::

        output = run_cmd('ls -l')
        for line in output.splitlines():
            print(line)

    :param args: list or string of shell command and arguments
    :returns: output of command

    """

    if isinstance(args, list):
        args = ' '.join(args)

    logging.debug('run_cmd: %s', args)

    try:
        result = subprocess.run(
            args,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            shell=True
        )
    except OSError as e:
        logging.error('Execution failed: %s', e)
        raise

    for line in result.stdout.splitlines():
        logging.debug('run_cmd output: %s', line)
    logging.debug('run_cmd %s returned %s', args, result.returncode)

    return result.stdout


def files(dir, ext=None):
    """Yield regular files in directory, optionally of specific extension.

    This function is a generator, and could be used like:

        for f in utils.files('/some/directory', 'pnm'):
            do_something_to_the_pnm(f)

    :param dir: directory to traverse
    :param ext: extension of files to list. Leading dot is ignored.

    """

    for f in os.scandir(dir):
        if not f.is_file():
            continue
        if ext and not f.name.endswith('.{}'.format(ext.lstrip('.'))):
            continue
        yield f.name


def move(old, new):
    """Move file

    :param old: file to move
    :param new: new location/filename

    """
    logging.debug('Renaming %s -> %s', old, new)
    shutil.move(old, new)


def remove(file):
    """Remove file.

    :param file: file to remove

    """
    logging.debug('Removing %s', file)
    os.remove(file)


def is_scan_name(name):
    """Determine whether name (probably) is the name of a scan directory.

    :param dir: directory name to check
    :returns: True if it is a scan directory, False if not.

    """
    try:
        datetime.datetime.strptime(name, config['Paths']['dir_format'])
    except ValueError:
        return False
    else:
        return True


def version():
    """Return sjkscan version.
    :returns: version string

    """
    return __version__


def parse_args(argv=None):
    """Parse command line arguments.

    :param argv: array of command line arguments (sys.argv)
    :returns: object with program arguments as attributes

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='%(prog)s v{}'.format(version()), help='print version and exit')
    parser.add_argument('-l', '--loglevel', type=str, help='log level')

    args = parser.parse_args(argv)

    if args.loglevel:
        if args.loglevel.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            config['Logging']['level'] = args.loglevel.upper()
            print('Log level is {}'.format(config['Logging']['level']))
        else:
            raise ValueError('{} is not a valid log level.', args.loglevel.upper())

    return args
