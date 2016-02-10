#!/usr/bin/env python
# encoding: utf-8

import os

from datetime import datetime
from sjkscan import scan


config = {
    'data_dir': '/Users/sjk/Code/sjkscan/data'
}


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    timestamp = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    unfinished = os.path.join(config['data_dir'], 'unfinished-' + timestamp)
    finished = os.path.join(config['data_dir'], 'scan-' + timestamp)
    output_dir = os.path.join(config['data_dir'], unfinished)

    try:
        os.mkdir(output_dir)
    except OSError as e:
        print('Could not create {}: {}', output_dir, e)

    scan.scan(output_dir)

    try:
        os.rename(unfinished, finished)
    except OSError as e:
        print('Could not rename {} to {}: {}', unfinished, finished, e)


if __name__ == '__main__':
    main()
