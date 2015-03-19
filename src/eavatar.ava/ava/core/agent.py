# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import gevent
from gevent import monkey
monkey.patch_all()

import os
import sys
import signal
import logging
import importlib
from ava.util import crypto
from ava.runtime import settings

from ava.spi import context
from ava.spi.defines import INSTALLED_ENGINES, AVA_SECRET_KEY, AVA_OWNER_XID
from ava.spi.signals import AGENT_STARTED, AGENT_STOPPING

logger = logging.getLogger(__name__)

__agent = None



def _mygetfilesystemencoding():
    old = sys.getfilesystemencoding

    def inner_func():
        ret = old()
        if ret is None:
            return 'UTF-8'
        else:
            return ret
    return inner_func


def patch_sys_getfilesystemencoding():
    # sys.getfilesystemencoding() always returns None when frozen on Ubuntu systems.
    patched_func = _mygetfilesystemencoding()
    sys.getfilesystemencoding = patched_func


def restart_later():
    if __agent.running:
        logger.warning("Agent not stopped successfully!")
    sys.exit(1)


def signal_handler(signum = None, frame = None):
    logger.debug("Received HUP signal, requests the shell to restart.")
    global __agent
    if __agent:
        __agent._stop_engines()
    sys.exit(1)


def load_class(full_class_string):
    """
    dynamically load a class from a string. e.g. 'a.b.package:classname'
    """

    class_data = full_class_string.split(":")
    module_path = class_data[0]
    class_name = class_data[1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return class_name, getattr(module, class_name)


class Agent(object):
    def __init__(self):
        logger.debug("Initializing agent...")
        patch_sys_getfilesystemencoding()

        self.running = False
        self.interrupted = False
        self._greenlets = []
        self._context = context.instance(self)
        self._engines = []
        self.__secret = None
        self.owner_xid = None

        self.get_security_keys()

        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_handler)

    def get_security_keys(self):
        self.__secret = os.environ.get(AVA_SECRET_KEY)
        self.owner_xid = os.environ.get(AVA_OWNER_XID)

        if self.__secret is None and not settings['debug']:
            logger.error('No agent secret is specified!')
            raise SystemExit(2)

        if self.owner_xid is None and not settings['debug']:
            logger.error(("No user XID is specified!"))
            raise SystemExit(2)

        if self.__secret:
            self.__secret = crypto.string_to_secret(self.__secret)
        elif settings['debug']:
            pk, sk = crypto.generate_keypair()
            self.__secret = sk

        if not self.owner_xid and settings['debug']:
            self.owner_xid = \
                b'AYPwK3c3VK7ZdBvKfcbV5EmmCZ8zSb9viZ288gKFBFuE92jE'

    def add_child_greenlet(self, child):
        self._greenlets.append(child)

    def _start_engines(self):
        for it in INSTALLED_ENGINES:
            logger.debug("Loading engine: %s", it)
            name, engine_cls = load_class(it)
            engine = engine_cls()

            self._context.bind(name, engine)
            self._engines.append(self._context[name])

        logger.debug("Starting engines...")
        for it in self._engines:
            it.start(self._context)

        self._context.send(signal=AGENT_STARTED, sender=self)

    def _stop_engines(self):
        self._context.send(signal=AGENT_STOPPING, sender=self)

        for it in reversed(self._engines):
            it.stop(self._context)

    def context(self):
        return self._context

    def run(self):
        logger.debug("Starting agent...")

        self._start_engines()

        self.running = True
        logger.debug("Agent started.")

        while not self.interrupted:
            try:
                gevent.joinall(self._greenlets, timeout=1)
            except KeyboardInterrupt:
                logger.debug("Interrupted.")
                break

        # stop engines in reverse order.
        self._stop_engines()

        gevent.killall(self._greenlets, timeout=1)

        self.running = False

        logger.debug("Agent stopped.")


def start_agent():
    global __agent
    __agent = Agent()
    __agent.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    start_agent()

