from models import Requestx
from util import set_cookie2cookies, merge_cookies


class Sessionx:

    def __init__(self):
        self.cookies = None
        self.res = None

    def head(self, url: str, **kwargs):
        return self.request("HEAD", url=url, **kwargs)

    def get(self, url: str, **kwargs):
        return self.request("GET", url=url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request("POST", url=url, **kwargs)

    def patch(self, url: str, **kwargs):
        return self.request("PATCH", url=url, **kwargs)

    def put(self, url: str, **kwargs):
        return self.request("PUT", url=url, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request("DELETE", url=url, **kwargs)

    def options(self, url: str, **kwargs):
        return self.request("OPTIONS", url=url, **kwargs)

    def request(self, method, url: str, fields=None, headers=None, cookies=None, body=None, json=None, timeout=None,
                retries=None, redirect=None, proxy=None):

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
            proxy=proxy
        )
        self.prepare_requestx(req)
        res = req.send()
        self.res = res
        return res

    def prepare_requestx(self, req: Requestx):
        """
        合并上下文以及请求中的Cookie，更新到req中
        :param req: Requestx实例化对象
        :return:
        """
        req_cookies = None
        res_cookies = None
        if "Cookie" in req.headers:
            # 请求有cookie
            req_cookies = req.headers["Cookie"]
            # print(req.headers["Cookie"])
        if self.res is not None:
            # 有上一个请求
            if "Set-Cookie" in self.res.headers:
                # 上一个请求中有Set-Cookie字段
                res_cookies = set_cookie2cookies(self.res.headers["Set-Cookie"])
        self.cookies = merge_cookies(self.cookies, req_cookies, res_cookies)
        # print(self.cookies)
        if self.cookies is not None and len(self.cookies) > 0:
            req.headers.update({"Cookie": self.cookies})
