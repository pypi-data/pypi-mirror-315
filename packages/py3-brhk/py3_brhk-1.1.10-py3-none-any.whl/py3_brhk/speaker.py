#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_brhk
=================================================
"""
from typing import Union

import py3_requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrls(py3_requests.RequestUrl):
    BASE = "https://speaker.17laimai.cn/"
    NOTIFY = "/notify.php"


class ValidatorJsonSchema(py3_requests.ValidatorJsonSchema):
    SUCCESS = Dict({
        "type": "object",
        "properties": {
            "errcode": {
                "oneOf": [
                    {"type": "integer", "const": 0},
                    {"type": "string", "const": "0"},
                ]
            }
        },
        "required": ["errcode"]
    })


class ResponseHandler(py3_requests.ResponseHandler):
    @staticmethod
    def success(response: Response = None):
        json_addict = ResponseHandler.status_code_200_json_addict(response=response)
        if Draft202012Validator(ValidatorJsonSchema.SUCCESS).is_valid(json_addict):
            return True
        return False


class Speaker(object):
    """
    brhk speaker class

    @see https://www.yuque.com/lingdutuandui
    """

    def __init__(
            self,
            base_url: str = RequestUrls.BASE,
            token: str = "",
            id: str = "",
            version: Union[int, str] = "1"
    ):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.token = token
        self.id = id
        self.version = version

    def notify(
            self,
            message: str = None,
            **kwargs
    ):
        """
        notify

        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#teXR7
        :param message:
        :param kwargs: py3_requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", py3_requests.RequestMethod.POST)
        kwargs.setdefault("response_handler", ResponseHandler.success())
        kwargs.setdefault("url", RequestUrls.NOTIFY)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("data", Dict())
        kwargs.data.setdefault("token", self.token)
        kwargs.data.setdefault("id", self.id)
        kwargs.data.setdefault("version", self.version)
        kwargs.data.setdefault("message", message)
        return py3_requests.request(
            **kwargs.to_dict()
        )
