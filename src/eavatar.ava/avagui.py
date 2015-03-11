#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The launcher for EAvatar to run in a text console or headless environment.
"""

import sys
import logging
import multiprocessing

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

# imports platform-specific dependencies.
if sys.platform.startswith('darwin'):
    import gui_osx
elif sys.platform.startswith('linux'):
    import gui_linux
elif sys.platform.startswith('win32'):
    import gui_win32

from ava.shell import factory

logger = logging.getLogger("ava")


def main():
    shell = factory.create()
    shell.do_run()

if __name__ == '__main__':
    sys.exit(main())