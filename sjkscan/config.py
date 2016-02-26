# -*- coding: utf-8 -*-
"""
    sjkscan.config
    ~~~~~~~~~~~~~~

    This module handles loading the configuration file and makes sure only
    proper settings are placed in the config dict.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""

import configparser

from pkg_resources import resource_string

config = dict()


def load_config(config_file=None):
    """Load the configuration file.

    Configuration options will be available in dict sjkscan.conf.config.
    When configuration options are added, modified or removed in future
    releases, `config_template` in this function must be updated.

    :param config_file: file to read. Defaults to sjkscan.conf in package bundle.

    """

    #: Dictionary of lists containing configuration file sections and entries.
    #: Each list contains tuples of configuration entry names and default values.
    #: If it's not in this dictionary, it doesn't make it to config.config.
    config_template = {
        'Paths': [
            ('data', '/Users/sjk/Code/sjkscan/data'),
            ('dir_format', '%Y-%m-%d_%H-%M-%S'),
            ('inbox', '%(data)s/INBOX'),
            ('archive', '%(data)s/ARCHIVE')
        ],
        'OCR': [
            ('language', 'swe')
        ],
        'Rotation': [
            ('rotatate', 180)
        ],
        'Scanimage': [
            ('resolution', 300),
            ('brightness', 80),
            ('contrast', 100)
        ],
        'Logging': [
            ('level', 'INFO')
        ]
    }

    # conf = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
    conf = configparser.ConfigParser()

    if config_file:
        conf.read(config_file)
    else:
        conf.read_string(resource_string(__name__, 'sjkscan.conf').decode('utf-8'))

    for section in config_template:
        config[section] = dict()
        for entry, default in config_template[section]:
            config[section][entry] = conf.get(section, entry, fallback=default)
