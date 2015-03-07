# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

logger = logging.getLogger(__name__)


class Sample(object):

    def __init__(self):
        logger.debug("Extension sample created.")

    def start(self, context):
        logger.debug("Hello from extension sample.")

    def stop(self, content):
        logger.debug("Sample extension stopped.")


