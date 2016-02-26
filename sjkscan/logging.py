# -*- coding: utf-8 -*-
"""
    sjkscan.logging
    ~~~~~~~~~~~~~~~

    This module handles logging related tasks, such as initialising the
    logging environment.

    :copyright: (c) 2016 by Svante Kvarnström
    :license: BSD, see LICENSE for more details.
"""
import logging


def init_logging(level):
    """Initialise logging.

    Set up basic logging.
    """
    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(level))

    logging.basicConfig(
        level=numeric_level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
    logging.debug('Initialising logging')
