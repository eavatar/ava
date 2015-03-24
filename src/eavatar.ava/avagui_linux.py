# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import gi.repository
from ctypes import cdll

cdll.LoadLibrary('libsodium.so')

from avagui import main


if __name__ == '__main__':
    main()
