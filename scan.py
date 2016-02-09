#!/usr/bin/env python
# encoding: utf-8

from sjkscan import sjkscan


def main():
    """TODO: docstring"""

    # sjkscan.ocr_pnms_in_dir('output', 'swe')
    sjkscan.merge_pdfs_in_dir('output', 'test.pdf')


if __name__ == '__main__':
    main()
