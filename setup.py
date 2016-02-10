#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='sjkscan',
    version='0.1.1a',
    packages=['sjkscan'],
    author=u'Svante Kvarnström',
    author_email='sjk@sjk.io',
    url='https://github.com/sjktje/sjkscan/',
    license='BSD',
    entry_points={
        'console_scripts': [
            'scan = sjkscan.scan:scan',
            'scand = sjkscan.postprocessing:scand'
        ]
    }
)
