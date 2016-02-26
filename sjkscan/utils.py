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

    :param args: list or string of shell command and arguments
    :returns: output of command

    """

    if isinstance(args, list):
        args = ' '.join(args)

    logging.debug('run_cmd: %s', args)

    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            shell=True).stdout
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


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
    # TODO: This should be a logger statement.
    print('Move: {} -> {}'.format(old, new))
    shutil.move(old, new)


def remove(file):
    """Remove file.

    :param file: file to remove

    """
    # TODO: This should be a logger statement.
    print('Remove: {}'.format(file))
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

    return parser.parse_args(argv)
