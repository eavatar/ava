# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.webfront import route

# sample resource

@route('/hello')
@route('/hello/')
def hello():
    return 'Hello, World'