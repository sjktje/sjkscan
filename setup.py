#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='sjkscan',
    version='0.1.1a',
    packages=['sjkscan'],
    package_data={
        'sjkscan': ['sjkscan.conf']
    },
    author=u'Svante Kvarnström',
    author_email='sjk@sjk.io',
    url='https://github.com/sjktje/sjkscan/',
    license='BSD',
    entry_points={
        'console_scripts': [
            'scan = sjkscan.scan:scan',
            'scand = sjkscan.postprocessing:scand'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ]
)
