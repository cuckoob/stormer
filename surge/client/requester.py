# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/12/13 13:57
"""
from urllib.parse import urljoin

import requests

from .respresult import RespResult
from ..utils.config import config
from ..utils.logger import logging

logger = logging.getLogger(__name__)


class Requester(object):
    """Requester is request Class which base on questions, it be used for send request."""

    def __init__(self, host, port=80, protocol="http", headers=None, config_module=None):
        """
        Init Requester
        :param config_module: config module
        """
        self.host = host
        self.port = port
        self.headers = headers
        self.protocol = protocol
        self.domain = "{}://{}".format(protocol, host)
        if port and int(port) != 80:
            self.domain = "{}:{}".format(self.domain, port)
        self.apis = []

        if config_module:
            try:
                config.from_obj(config_module)
            except Exception as e:
                logger.error("Error: set config fail, Detail: {}".format(e))

    @staticmethod
    def set_config_module(module):
        try:
            config.from_obj(module)
        except Exception as e:
            logger.error("Error: set config fail, Detail: {}".format(e))

    @staticmethod
    def _path_url(url, path_params):
        if path_params and isinstance(path_params, dict):
            url = url.format(**path_params)
        return url

    def _bind_func(self, pre_url, action):
        def req(path_params=None, params=None, data=None, json=None, files=None, headers=None, **kwargs):
            url = self._path_url(pre_url, path_params)
            resp = self._do_request(action, url, params, data, json, files, headers, **kwargs)
            return RespResult(resp, url, action)

        return req

    def _add_path(self, action, uri, func_name):
        action = action.upper()
        func_name = func_name.lower()
        assert func_name not in self.apis, u"Duplicate function <{}>.".format(func_name)
        url = urljoin(self.domain, uri)
        setattr(self, func_name, self._bind_func(url, action))
        self.apis.append(func_name)
        return getattr(self, func_name)

    @staticmethod
    def _func_name(func):
        try:
            func_name = func.__name__
        except (Exception,):
            func_name = str(func)
        return func_name

    def register(self, action, func, uri):
        func_name = self._func_name(func)
        return self._add_path(action, uri, func_name)

    def _headers(self, headers):
        """combine headers"""
        if headers and isinstance(headers, dict):
            if self.headers:
                for key, value in self.headers.items():
                    if key in headers:
                        continue
                    headers[key] = value
        else:
            headers = self.headers
        return headers

    def _do_request(self, action, url, params=None, data=None, json=None, files=None, headers=None, **kwargs):
        headers = self._headers(headers)
        if action.upper() == "GET":
            return self.get(url, params=params, headers=headers, **kwargs)
        if action.upper() == "POST":
            return self.post(url, data=data, json=json, files=files, headers=headers, **kwargs)
        if action.upper() == "PUT":
            return self.put(url, data=data, json=json, files=files, headers=headers, **kwargs)
        if action.upper() == "DELETE":
            return self.delete(url, headers=headers, **kwargs)
        if action.upper() == "OPTIONS":
            return self.options(url, headers=headers, **kwargs)

    @staticmethod
    def get(url, params=None, headers=None, **kwargs):
        assert url, u"url不能为空."
        assert (not params or isinstance(params, dict)), u"params参数类型错误."
        return requests.get(url, params=params, headers=headers, **kwargs)

    @staticmethod
    def post(url, data=None, json=None, files=None, headers=None, **kwargs):
        assert url, u"url不能为空."
        assert (not data or isinstance(data, dict)), u"data参数类型错误."
        assert (not json or isinstance(json, dict)), u"json参数类型错误."
        assert (not files or isinstance(files, (list, tuple, dict))), u"files参数类型错误."
        return requests.post(url, data=data, json=json, files=files, headers=headers, **kwargs)

    @staticmethod
    def put(url, data=None, json=None, files=None, headers=None, **kwargs):
        assert url, u"url不能为空."
        assert (not data or isinstance(data, dict)), u"data参数类型错误."
        assert (not json or isinstance(json, dict)), u"json参数类型错误."
        assert (not files or isinstance(files, (list, tuple, dict))), u"files参数类型错误."
        return requests.put(url, data=data, json=json, files=files, headers=headers, **kwargs)

    @staticmethod
    def delete(url, headers=None, **kwargs):
        assert url, u"url不能为空."
        return requests.delete(url, headers=headers, **kwargs)

    @staticmethod
    def options(url, headers=None, **kwargs):
        assert url, u"url不能为空."
        return requests.options(url, headers=headers, **kwargs)
