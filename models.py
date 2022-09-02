# coding=utf-8
import os
import sys

import urllib3
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from util import dict2cookies, random_ua

try:
    from urllib3.contrib.socks import SOCKSProxyManager
except ImportError:
    def SOCKSProxyManager(*args, **kwargs):
        raise ImportError("Missing dependencies [SOCKSProxyManager from urllib3.contrib.socks] for SOCKS support.")


class Requestx:

    def __init__(self, method, url, fields, headers, cookies, body, json_data, timeout, retries, redirect, proxy):
        """
        实例化urllib3的Pool(SOCKSProxy/Proxy)Manager，并设置对应参数
        :param method: 请求方法，必须大写
        :param url: 目标url，需要指定协议
        :param fields: 表单数据，使用multipart-form进行传输
        :param headers: 请求头，若为空，则会随机使用UA头，且在不适用表单(fields)和json_data时，POST和PUT会默认使用x-www-form-urlencoded
        :param cookies: cookie，必须使用字典或`UUID=1234; _TZ=6789`的格式
        :param body: body部分数据
        :param json_data: 使用json传输数据包，自动设置Content-Type
        :param timeout: 超时时间，默认为5s
        :param retries: 重试次数，默认为2
        :param redirect: 是否允许重定向，默认不允许
        :param proxy: 代理url，置空表示不适用代理

        示例详见test.py文件
        """
        self.timeout = timeout or 5
        self.retries = retries or 2
        self.redirect = True if redirect is None or redirect else False
        self.proxy = proxy
        if proxy is not None:
            if isinstance(proxy, str):
                if proxy.startswith("socks4a://") or proxy.startswith("socks5h://"):
                    self.http = SOCKSProxyManager(proxy_url=proxy, timeout=self.timeout, retries=self.retries)
                elif proxy.startswith("http://") or proxy.startswith("https://"):
                    self.http = urllib3.ProxyManager(proxy_url=proxy, timeout=self.timeout, retries=self.retries)
                else:
                    raise ValueError("proxy type error. example: http(s)://127.0.0.1:8080, socks4a://127.0.0.1:8080, socks5h://127.0.0.1:8080")
            else:
                raise ValueError("proxy must be string. example: http(s)://127.0.0.1:8080, socks4a://127.0.0.1:8080, socks5h://127.0.0.1:8080")
        else:
            self.http = urllib3.PoolManager(timeout=self.timeout, retries=self.retries)
        # 判断是否有代理，并设置timeout, redirect, proxy
        self.method = method
        self.url = url
        self.fields = fields
        self.headers = headers or {}
        # 所有请求随机user-agent
        if "User-Agent" not in self.headers.keys():
            self.headers.update({"User-Agent": random_ua()})
        # post/put默认content-type为x-www-form-urlencoded
        if fields is None and json_data is None:
            if self.method in ["POST", "PUT"]:
                if "Content-Type" not in self.headers.keys():
                    self.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        # 设置cookies
        if cookies is not None:
            if isinstance(cookies, dict):
                cookies_ = dict2cookies(cookies)
                self.headers.update({"Cookie": cookies_})
            elif isinstance(cookies, str):
                self.headers.update({"Cookie": cookies})
            else:
                raise ValueError("Cookie should be dict or string. example: {'SESSIONID': ABCDEFG}, 'SESSIONID=ABCDEFG'")
        # body为json
        if json_data is not None:
            if isinstance(json_data, dict):
                self.body = json.dumps(json_data).encode("utf-8")
                self.headers.update({"Content-Type": "application/json"})
            else:
                raise ValueError("json_data must be dict. example: {'a': 1}")
        else:
            self.body = body

    def __repr__(self):
        return f'<Requestx [{self.method}]>'

    def send(self):
        """
        发送请求
        """
        if self.fields is not None and self.body is not None:
            raise TypeError("request got values for both 'fields' and 'body', can only specify one.")
        if self.fields is None:
            native_res = self.http.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                body=self.body,
                redirect=self.redirect
            )
        else:
            native_res = self.http.request(
                method=self.method,
                url=self.url,
                fields=self.fields,
                headers=self.headers,
                redirect=self.redirect
            )
        return Responsex(self, native_res)


class Responsex:
    """
    用于包装urllib3的Response对象
    """
    def __init__(self, req: Requestx, native_res: urllib3.response.HTTPResponse):
        self.request = req
        self.native_res = native_res
        self.content = native_res.data
        self.text = native_res.data.decode()
        self.headers = native_res.headers
        self.status_code = native_res.status

    def __repr__(self):
        return f'<Responsex [{self.status_code}]>'

