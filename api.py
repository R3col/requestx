# coding=utf-8
"""
该文件为requestx模块的对外接口
"""
from models import Requestx
from sessions import Sessionx


def head(url: str, **kwargs):
    return request("HEAD", url=url, **kwargs)


def get(url: str, **kwargs):
    return request("GET", url=url, **kwargs)


def post(url: str, **kwargs):
    return request("POST", url=url, **kwargs)


def patch(url: str, **kwargs):
    return request("PATCH", url=url, **kwargs)


def put(url: str, **kwargs):
    return request("PUT", url=url, **kwargs)


def delete(url: str, **kwargs):
    return request("DELETE", url=url, **kwargs)


def options(url: str, **kwargs):
    return request("OPTIONS", url=url, **kwargs)


def request(method, url: str, fields=None, headers=None, cookies=None, body=None, json=None, timeout=None, retries=None, redirect=None, proxy=None):
    req = Requestx(
        method=method,
        url=url,
        fields=fields,
        headers=headers,
        cookies=cookies,
        body=body,
        json_data=json,
        timeout=timeout,
        retries=retries,
        redirect=redirect,
        proxy=proxy,
    )
    res = req.send()
    return res


def session():
    """
    使用Sessionx客户端，会自动更新Cookie
    :return: Sessionx实例化对象
    """
    return Sessionx()
















