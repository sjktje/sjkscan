#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import time

from sjkscan import postprocessing


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    DATA_DIR = '/Users/sjk/Code/sjkscan/data'
    while True:
        for entry in os.scandir(DATA_DIR):
            if not entry.name.startswith('finished-') or not entry.is_dir():
                continue

            scan_dir = os.path.join(DATA_DIR, entry.name)

            postprocessing.move_blanks(scan_dir,
                                       os.path.join(scan_dir, 'blank'))

            postprocessing.rotate_all_images_in_dir(scan_dir, 180)

            postprocessing.ocr_pnms_in_dir(scan_dir, 'swe')

            pdf_output = os.path.join(scan_dir, 'output.pdf')
            postprocessing.merge_pdfs_in_dir(scan_dir, pdf_output)

            inbox_dir = os.path.join(DATA_DIR, 'INBOX')

            try:
                os.mkdir(inbox_dir)
            except:
                pass  # Assume directory exists.

            shutil.move(scan_dir, inbox_dir)

        time.sleep(1)


if __name__ == "__main__":
    main()
