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


logger = logging.getLogger("ava")


def main():
    from ava.cmds.cli import cli, load_commands

    load_commands()
    return cli(auto_envvar_prefix='AVA')

if __name__ == '__main__':
    sys.exit(main())