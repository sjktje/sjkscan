#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sjkscan

setup(
    name='sjkscan',
    version=sjkscan.__version__,
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
            'scan = sjkscan.scan:main',
            'scand = sjkscan.postprocessing:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ]
)
