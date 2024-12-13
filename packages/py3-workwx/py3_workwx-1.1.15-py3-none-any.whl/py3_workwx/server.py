#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_workwx
=================================================
"""
from datetime import timedelta
from typing import Union

import diskcache
import py3_requests
import redis
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl(py3_requests.RequestUrl):
    BASE = "https://qyapi.weixin.qq.com/"
    GET_API_DOMAIN_IP = "/cgi-bin/get_api_domain_ip"
    GETTOKEN = "/cgi-bin/gettoken"
    MESSAGE_SEND = "/cgi-bin/message/send"
    MEDIA_UPLOAD = "/cgi-bin/media/upload"
    MEDIA_UPLOADIMG = "/cgi-bin/media/uploadimg"


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
        "required": ["errcode"],
    })

    GETTOKEN = Dict({
        "type": "object",
        "properties": {
            "access_token": {"type": "string", "minLength": 1},
        },
        "required": ["access_token"],
    })

    GET_API_DOMAIN_IP = Dict({
        "type": "object",
        "properties": {
            "ip_list": {"type": "array", "minItem": 1},
        },
        "required": ["ip_list"],
    })

    MEDIA_UPLOAD = Dict({
        "type": "object",
        "properties": {
            "media_id": {"type": "string", "minLength": 1},
        },
        "required": ["media_id"],
    })

    MEDIA_UPLOADIMG = Dict({
        "type": "object",
        "properties": {
            "url": {"type": "string", "minLength": 1},
        },
        "required": ["url"],
    })


class ResponseHandler(py3_requests.ResponseHandler):
    @staticmethod
    def success(response: Response = None):
        json_addict = ResponseHandler.status_code_200_json_addict(response=response)
        if Draft202012Validator(ValidatorJsonSchema.SUCCESS.to_dict()).is_valid(instance=json_addict):
            return json_addict
        return None


class Server:
    def __init__(
            self,
            base_url: str = RequestUrl.BASE,
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None
    ):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.cache = cache

    def request_with_token(self, **kwargs):
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", "")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.params.setdefault("access_token", self.access_token)
        return py3_requests.request(**kwargs.to_dict())

    def get_api_domain_ip(self, **kwargs):
        """
        get_api_domain_ip

        @see https://developer.work.weixin.qq.com/document/path/92520
        :param kwargs: requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", RequestUrl.GET_API_DOMAIN_IP)
        result = self.request_with_token(**kwargs.to_dict());
        if Draft202012Validator(ValidatorJsonSchema.GET_API_DOMAIN_IP).is_valid(result):
            return result.get("ip_list", None)
        return None

    def gettoken_with_cache(
            self,
            expire: Union[float, int, timedelta] = 7100,
            gettoken_kwargs: dict = {},
            get_api_domain_ip_kwargs: dict = {}
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param gettoken_kwargs: self.gettoken kwargs
        :param get_api_domain_ip_kwargs: self.get_api_domain_ip kwargs
        :return:
        """
        gettoken_kwargs = Dict(gettoken_kwargs)
        get_api_domain_ip_kwargs = Dict(get_api_domain_ip_kwargs)
        cache_key = f"py3_workwx_access_token_{self.agentid}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)
        if not Draft202012Validator(ValidatorJsonSchema.GET_API_DOMAIN_IP).is_valid(
                self.get_api_domain_ip(**get_api_domain_ip_kwargs.to_dict())
        ):
            self.gettoken(**gettoken_kwargs.to_dict())

            if isinstance(self.access_token, str) and len(self.access_token):
                if isinstance(self.cache, diskcache.Cache):
                    self.cache.set(
                        key=cache_key,
                        value=self.access_token,
                        expire=expire or timedelta(seconds=7100).total_seconds()
                    )
                if isinstance(self.cache, (redis.Redis, redis.StrictRedis)):
                    self.cache.setex(
                        name=cache_key,
                        value=self.access_token,
                        time=expire or timedelta(seconds=7100),
                    )
        return self

    def gettoken(self, **kwargs):
        """
        gettoken

        @see https://developer.work.weixin.qq.com/document/path/91039
        :param kwargs: py3_requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", RequestUrl.GETTOKEN)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.params.setdefault("corpid", self.corpid)
        kwargs.params.setdefault("corpsecret", self.corpsecret)
        result = py3_requests.request(
            **kwargs.to_dict(),
        )
        if Draft202012Validator(ValidatorJsonSchema.GETTOKEN).is_valid(result):
            self.access_token = result.get("access_token", None)

        return self

    def message_send(self, **kwargs):
        """

        @see https://developer.work.weixin.qq.com/document/path/90236
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MESSAGE_SEND)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        return self.request_with_token(**kwargs.to_dict())

    def media_upload(self, types="file", **kwargs):
        """
        @see https://developer.work.weixin.qq.com/document/path/90253
        :param types:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MEDIA_UPLOAD)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        types = "file" if types.lower() not in ["file", "image", "voice", "video"] else types
        kwargs.params.setdefault("type", types)
        result = self.request_with_token(**kwargs.to_dict())
        if Draft202012Validator(ValidatorJsonSchema.MEDIA_UPLOAD).is_valid(result):
            return result.get("media_id", None)
        return None

    def meida_uploadimg(self, **kwargs):
        """
        @see https://developer.work.weixin.qq.com/document/path/90256
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", RequestUrl.MEDIA_UPLOADIMG)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        result = self.request_with_token(**kwargs.to_dict())
        if Draft202012Validator(ValidatorJsonSchema.MEDIA_UPLOADIMG).is_valid(result):
            return result.get("url", None)
        return None
