# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import click


from .cli import cli

logger = logging.getLogger(__name__)


@cli.command()
def run():
    from ava.shell.console import Shell
    logger.debug("Starting the shell...")
    shell = Shell()
    shell.do_run()
    logger.debug("Shell stopped.")
