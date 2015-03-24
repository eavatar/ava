# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import win32api
import win32gui
import win32gui_struct
from ctypes import cdll

cdll.LoadLibrary('libsodium')

from avagui import main

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui


if __name__ == '__main__':
    main()