# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/12/13 13:57
"""
from __future__ import absolute_import, unicode_literals

from collections import namedtuple

import requests

from surge.utils.constants import UNKNOWN_ERROR, MSG, GONE_AWAY

Resp = namedtuple("Resp", ["status_code", "code", "data", "msg"])


class RespResult(object):
    """
    Used for packing request response
    """

    def __init__(self, resp=None, url=None, action=None):
        if resp and not isinstance(resp, requests.Response):
            raise Exception("Param<resp> should be object of requests.Response, but {} found.".format(type(resp)))
        self.resp = resp
        self.status = resp.ok
        self.reason = resp.reason
        self.content = resp.content
        self.headers = resp.headers.__repr__()
        self.encoding = resp.encoding
        self.status_code = resp.status_code
        self.req_url = url
        self.req_action = action

    @property
    def bytes(self):
        return self.content

    @property
    def text(self):
        return self.resp.text

    @property
    def json(self):
        return self.resp.json

    @property
    def json_resp(self):
        """parse resp to api resp"""
        if not self.resp:
            return Resp(status_code=400, code=UNKNOWN_ERROR, data=None, msg=MSG[UNKNOWN_ERROR])
        if 200 <= self.status_code < 300:
            code = (self.json or {}).get("code", GONE_AWAY)
            if code:
                return Resp(status_code=self.status_code, code=code, data=None, msg=(self.json or {}).get("message"))
            return Resp(status_code=self.status_code, code=code, data=self.json, msg=MSG.get(code))
        if isinstance(self.reason, bytes):
            try:
                reason = self.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')
        else:
            reason = self.reason
        return Resp(status_code=self.status_code, code=UNKNOWN_ERROR, data=None, msg=reason)
