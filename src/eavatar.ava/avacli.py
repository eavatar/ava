#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The launcher for EAvatar to run in a text console or headless environment.
"""

import os
import sys
import logging
import multiprocessing

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()
import pkg_resources

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


def package_in_path(pkg):
    for path in sys.path:
        if pkg in path:
            return True
    return False


def setup_eggs_folder():
    # add packages in 'eggs' to sys.path in case PyInstaller haven't done that.
    if hasattr(sys, "_MEIPASS") and not package_in_path('eavatar.core'):
        logger.debug("'eggs' not in path, try to add them.")
        eggs_dir = os.path.join(sys._MEIPASS, 'eggs')
        logger.debug("Core packages path: %s", eggs_dir)
        distributions, errors = pkg_resources.working_set.find_plugins(
            pkg_resources.Environment([eggs_dir])
        )

        for it in distributions:
            logger.debug("Added package: %s", it.project_name)
            pkg_resources.working_set.add(it)

        if len(errors) > 0:
            logger.error("failed to load package(s): %s", errors)


def main():

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG, disable_existing_loggers=False)

    setup_eggs_folder()

    from ava.cmds import cli

    cli(auto_envvar_prefix='AVA')

if __name__ == '__main__':
    main()