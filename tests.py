# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/12/13 15:56
"""
from __future__ import absolute_import, unicode_literals

from stormer import Requester

if __name__ == '__main__':
    requester = Requester("http://www.baidu.com")

    requester.register(action="get", func="bd_download", uri="download")

    rlt = requester.bd_download()
    r_byte = rlt.bytes
    print(r_byte)