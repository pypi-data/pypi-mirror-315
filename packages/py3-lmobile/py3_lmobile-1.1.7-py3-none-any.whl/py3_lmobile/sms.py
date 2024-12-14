#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_lmobile
=================================================
"""
import hashlib
import string
from datetime import datetime
import random
from typing import Union

import py3_requests
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl(py3_requests.RequestUrl):
    BASE = "https://api.51welink.com/"
    SEND_SMS = "/EncryptionSubmit/SendSms.ashx"


class ValidatorJsonSchema(py3_requests.ValidatorJsonSchema):
    SUCCESS = Dict({
        "type": "object",
        "properties": {
            "Result": {"type": "string", "const": "succ"},
        },
        "required": ["Result"]
    })


class ResponseHandler(py3_requests.ResponseHandler):
    @staticmethod
    def success(response: Response = None):
        json_addict = ResponseHandler.status_code_200_json_addict(response=response)
        if Draft202012Validator(ValidatorJsonSchema.SUCCESS).is_valid(instance=json_addict):
            return True
        return False


class Sms(object):
    """
    @see https://www.lmobile.cn/ApiPages/index.html
    """

    def __init__(
            self,
            base_url: str = RequestUrl.BASE,
            account_id: str = "",
            password: str = "",
            product_id: Union[int, str] = 0,
            smms_encrypt_key: str = "SMmsEncryptKey",
    ):
        """
        @see https://www.lmobile.cn/ApiPages/index.html
        :param base_url:
        :param account_id:
        :param password:
        :param product_id:
        :param smms_encrypt_key:
        """
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.account_id = account_id
        self.password = password
        self.product_id = product_id
        self.smms_encrypt_key = smms_encrypt_key

    def timestamp(self):
        return int(datetime.now().timestamp())

    def random_digits(self, length=10):
        return int("".join(random.sample(string.digits, length)))

    def password_md5(self):
        return hashlib.md5(f"{self.password}{self.smms_encrypt_key}".encode('utf-8')).hexdigest()

    def sha256_signature(self, data: dict = {}):
        data = Dict(data)
        data.setdefault("AccountId", self.account_id)
        data.setdefault("Timestamp", self.timestamp())
        data.setdefault("Random", self.random_digits())
        data.setdefault("ProductId", self.product_id)
        data.setdefault("PhoneNos", "")
        data.setdefault("Content", "")
        temp_string = "&".join([
            f"AccountId={data.get("AccountId", "")}",
            f"PhoneNos={str(data.get("PhoneNos", "")).split(",")[0]}",
            f"Password={self.password_md5().upper()}",
            f"Random={data.get('Random', "")}",
            f"Timestamp={data.get('Timestamp', "")}",
        ])
        return hashlib.sha256(temp_string.encode("utf-8")).hexdigest()

    def send_sms(
            self,
            phone_nos: str = None,
            content: str = None,
            **kwargs
    ):
        """
        @see https://www.lmobile.cn/ApiPages/index.html
        :param phone_nos:
        :param content:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", py3_requests.RequestMethod.POST)
        kwargs.setdefault("url", RequestUrl.SEND_SMS)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("data", Dict())
        kwargs.data.setdefault("AccountId", self.account_id)
        kwargs.data.setdefault("Timestamp", self.timestamp())
        kwargs.data.setdefault("Random", self.random_digits())
        kwargs.data.setdefault("ProductId", self.product_id)
        kwargs.data.setdefault("PhoneNos", phone_nos)
        kwargs.data.setdefault("Content", content)
        kwargs.data.setdefault("AccessKey", self.sha256_signature(kwargs.data))
        return py3_requests.request(**kwargs.to_dict())
