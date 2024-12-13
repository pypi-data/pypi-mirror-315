#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_requests
=================================================
"""
from typing import Callable

import requests
from addict import Dict
from bs4 import BeautifulSoup
from requests import Response


class RequestUrl(object):
    """
    request url class
    """
    pass


class ValidatorJsonSchema(object):
    """
    validate json schema class
    """
    pass


class ResponseHandler(object):
    """
    response handler class
    """

    @staticmethod
    def status_code_200_text(response: Response = None):
        """
        get response.text
        :param response: requests.Response instance
        :return: response.text= if response.status_code==200 else None
        """
        if isinstance(response, Response) and response.status_code == 200:
            return response.text
        return None

    @staticmethod
    def status_code_200_beautifulsoup(response: Response = None, beautifulsoup_kwargs: dict = None):
        """
        get bs4.BeautifulSoup instance
        :param response: requests.Response instance
        :param beautifulsoup_kwargs: bs4.BeautifulSoup kwargs
        :return: bs4.BeautifulSoup instance if isinstance(text, str) and len(text) else None
        """
        text = RequestHandler.status_code_200_text(response=response)
        if isinstance(text, str) and len(text):
            return BeautifulSoup(text, **Dict(beautifulsoup_kwargs).to_dict())
        return None

    @staticmethod
    def status_code_200_json(response: Response = None, json_kwargs: dict = None):
        """
        get response.json()
        :param response: requests.Response instance
        :param json_kwargs: response.json() kwargs
        :return: response.json() if response.status_code==200 else None
        """
        if isinstance(response, Response) and response.status_code == 200:
            return response.json(**Dict(json_kwargs).to_dict())
        return None

    @staticmethod
    def status_code_200_json_addict(response: Response = None, **json_kwargs):
        """
        get addict.Dict(response.json())
        :param response: requests.Response instance
        :param json_kwargs: response.json() kwargs
        :return:  addict.Dict(response.json()) if response.status_code==200 else addict.Dict()
        """
        return Dict(RequestHandler.status_code_200_json(response=response, **json_kwargs))


def request(response_handler: Callable = None, *args, **kwargs):
    """
    requests request function extension

    @see requests document https://requests.readthedocs.io/en/latest/
    :param response_handler: response handler function
    :param args: requests.request args
    :param kwargs: requests.request kwargs
    :return: response_handler(response) if isinstance(response_handler, Callable) else response
    """
    kwargs = Dict(kwargs)
    response: Response = requests.request(*args, **kwargs.to_dict())
    if isinstance(response_handler, Callable):
        return response_handler(response)
    return response
