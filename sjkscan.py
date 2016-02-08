#!/usr/bin/env python
# encoding: utf-8

from sjkscan import *


def main():
    """TODO: docstring"""
    output_dir = 'output'
    scan(output_dir)

    for f in os.scandir(output_dir):
        if not f.is_file():
            next
        remove_if_blank(os.path.join(output_dir, f.name))


    rotate_all_images_in_dir(output_dir, 180)


if __name__ == '__main__':
    main()
