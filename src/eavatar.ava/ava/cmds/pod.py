# -*- coding: utf-8 -*-
"""
Command for managing local pod directory.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import click

from .cli import cli


@cli.group()
def pod():
    """ Pod management commands
    """
    pass

@pod.command()
@click.argument("folder", type=click.Path(exists=False))
def init(folder):
    if os.path.exists(folder):
        click.echo("Folder %s is not empty!" % folder, err=True)
        return

    click.echo("Initializing pod folder at %s" % folder)