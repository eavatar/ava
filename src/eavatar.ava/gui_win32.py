# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import win32api
import win32gui
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

