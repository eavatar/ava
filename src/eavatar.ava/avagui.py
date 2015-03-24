#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The launcher for EAvatar to run in a text console or headless environment.
"""

import os
import sys
import logging
import multiprocessing
from ava.runtime import environ

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()

# imports dependencies for PyInstaller to figure out what to include.
import depends

# prevent IDE regarding depends as not used.
depends.absolute_import


# prevent no handler warning
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


from ava.shell import factory

logger = logging.getLogger("ava")


def main():
    os.chdir(environ.base_dir())
    from libnacl import _get_nacl
    _get_nacl()

    shell = factory.create()
    shell.do_run()

if __name__ == '__main__':
    sys.exit(main())