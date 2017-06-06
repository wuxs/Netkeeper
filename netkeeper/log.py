# coding=utf-8
import logging
import os

from settings import LOG_FILE


def _getLogger():
    logger = logging.getLogger('[NkService]')
    handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = _getLogger()
