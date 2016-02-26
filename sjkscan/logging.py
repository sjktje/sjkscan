import logging


def init_logging():
    """Initialise logging.

    Set up basic logging.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
    logging.debug('Initialising logging')
