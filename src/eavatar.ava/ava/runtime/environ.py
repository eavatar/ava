# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

HOME_DIR_ENV = 'AVA_HOME'
PROFILE_ENV = 'AVA_PROFILE'

HOME_DIR_NAME = u'home'
PKGS_DIR_NAME = u'pkgs'
LOGS_DIR_NAME = u'logs'
DATA_DIR_NAME = u'data'
CONF_DIR_NAME = u'conf'


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)
_logger = logging.getLogger(__name__)


class Environment(object):
    """
    Encapsulates the runtime environment.
    """
    def __init__(self, home=None, a_profile=None):

        # Determines the location of the base directory which contains files shared by all users.
        # This script assumes it is located at 'eavatar/runtime' sub-directory.
        from ava.util import base_path

        self.base_dir = base_path()

        # Determines the location of the home directory.

        self.home_dir = os.path.join(self.base_dir, HOME_DIR_NAME)

        self.home_dir = os.path.abspath(self.home_dir)
        self.conf_dir = os.path.join(self.home_dir, CONF_DIR_NAME)
        self.pkgs_dir = os.path.join(self.home_dir, PKGS_DIR_NAME)
        self.data_dir = os.path.join(self.home_dir, DATA_DIR_NAME)
        self.logs_dir = os.path.join(self.home_dir, LOGS_DIR_NAME)

        _logger.debug("Home dir: %s", self.home_dir)

        # Flag indicating if the runtime is launched by a shell.
        self.has_shell = False
        self.shell_port = 0



# The global environment.
_environ = None


def get_environ(home=None, profile=None):
    global _environ

    if _environ is None:
        _environ = Environment(home, profile)

    return _environ


def base_dir():
    """
    Gets the base directory.
    :return:
    """
    return get_environ().base_dir


def home_dir():
    """
    Gets the home directory.
    :return:
    """
    return get_environ().home_dir


def conf_dir():
    """
    Gets the path for configuration files.

    :return: The configuration path.
    """
    return get_environ().conf_dir


def data_dir():
    """
    Gets the path for data files.

    :return: The path.
    """
    return get_environ().data_dir


def logs_dir():
    """
    Gets the path for log files.

    :return: The path.
    """
    return get_environ().logs_dir


def pkgs_dir():
    """
    Gets the path for packages files.

    :return: The path.
    """
    return get_environ().pkgs_dir



