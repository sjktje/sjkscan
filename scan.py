#!/usr/bin/env python
# encoding: utf-8

from sjkscan import sjkscan
import os


def main():
    """TODO: docstring"""

    files_to_merge = []

    for file in os.scandir('/Users/sjk/scan/'):
        if not file.is_file():
            next
        if (file.name[:4] != '.pdf'):
            next
        files_to_merge.append(os.path.join('/Users/sjk/scan', file.name))

    sjkscan.merge_pdfs(files_to_merge, '/Users/sjk/Code/scan/output.pdf')


if __name__ == '__main__':
    main()
