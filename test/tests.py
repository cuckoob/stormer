#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function

import unittest

from stormer import Requester


class TestClient(unittest.TestCase):
    def test_get_server(self):
        requester = Requester(
            server_url="http://www.baidu.com",
            # redis_url="redis://127.0.0.1:6379/0",
            timeout=30 * 60
        )

        requester.register(action="get", func="bd_download", uri="/")

        rlt = requester.bd_download()
        r_byte = rlt.bytes
        print(r_byte)

        self.assertEqual(rlt.status_code, 200)


if __name__ == '__main__':
    unittest.main()
