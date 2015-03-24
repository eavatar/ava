# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import os

import AppKit
from AppKit import *

from ctypes import cdll
from ava.runtime import environ


#nacl = cdll.LoadLibrary(os.path.join(environ.base_dir(), 'libsodium.dylib'))

# workaround for loading libsodium.dylib on Mac OSX
os.chdir(environ.base_dir())


import avagui
from avagui import main


if __name__ == '__main__':
    main()