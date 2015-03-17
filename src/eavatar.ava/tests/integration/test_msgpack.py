# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import unittest
from io import BytesIO
from msgpack import Packer, Unpacker, packb, unpackb



class MsgPackTest(unittest.TestCase):

    def test_packer_unpacker(self):
        buf = BytesIO()
        packer = Packer()
        buf.write(packer.pack(1))
        buf.write(packer.pack('2'))
        buf.write(packer.pack({}))
        buf.seek(0)
        unpacker = Unpacker(buf)
        v1 = unpacker.unpack()
        self.assertEqual(1, v1)

        v2 = unpacker.unpack()
        self.assertEqual('2', v2)

        v3 = unpacker.unpack()
        self.assertTrue(isinstance(v3, dict))

