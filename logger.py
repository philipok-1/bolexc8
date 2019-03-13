'''logging utility'''

import logging
import sys


def loggerMaster(name, logfile='default.log', logLevel='NOTSET'):

    """master function to create loggers"""

    numeric_level = getattr(logging, logLevel.upper(), 10)

    logger = logging.getLogger(str(name))
    logger.setLevel(level=logLevel)
    fh = logging.FileHandler(logfile, mode="a")
    fh.setLevel(level=logLevel)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level=logLevel)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate=False

    return logger
