# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

from ctypes import cdll

cdll.LoadLibrary('libsodium.so')
