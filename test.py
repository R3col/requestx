from api import *
import urllib3
import json


def test_get():
    # get请求测试
    res = get(url="http://httpbin.org/get")
    print(res.text)
    assert res.status_code == 200
    # get 参数测试
    res = get(url="http://httpbin.org/get?a=1&b=2")
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["args"] == {"a": "1", "b": "2"}


def test_cookies():
    # 字符串格式cookies测试
    res = get(url="http://httpbin.org/cookies", cookies="Test=123456; Testb=222")
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["cookies"] == {"Test": "123456", "Testb": "222"}
    # 字典格式cookies测试
    res = get(url="http://httpbin.org/cookies", cookies={"Test": "123456", "Testb": "222"})
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["cookies"] == {"Test": "123456", "Testb": "222"}


def test_headers():
    # 请求头测试
    # 自定义请求头
    res = get(url="http://httpbin.org/headers", headers={"Test": "asd"})
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["headers"]["Test"] == "asd"
    # UA头
    res = get(url="http://httpbin.org/headers", headers={"User-Agent": "test"})
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["headers"]["User-Agent"] == "test"


def test_post():
    # post方法测试
    # post参数测试 --> fields 用于multipart/form-data 传输
    res = post(url="http://httpbin.org/post", fields={"q": "1"})
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["form"] == {"q": "1"}
    # post参数测试 --> body 用于任意自定义参数传输，默认x-www-form-urlencoded
    res = post(url="http://httpbin.org/post", body="q=1")
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["form"] == {"q": "1"}


def test_json():
    # json格式传输测试
    res = post(url="http://httpbin.org/post", json={"q": "1"})
    print(res.text)
    json_ = json.loads(res.text)
    assert json_["json"] == {"q": "1"}


def test_proxy():
    # 代理测试
    # http代理
    res = get(url="http://httpbin.org/get", proxy="http://127.0.0.1:8080")
    print(res.status_code)
    assert res.status_code == 200
    # socks5代理
    res = get(url="http://httpbin.org/get", proxy="socks5h://test:1234@127.0.0.1:1088")
    print(res.status_code)
    assert res.status_code == 200
    # socks4代理
    res = get(url="http://httpbin.org/get", proxy="socks4a://127.0.0.1:1088")
    print(res.status_code)
    assert res.status_code == 200


def test_redirect():
    # 重定向测试 ---> 默认允许重定向
    res = post(url="http://httpbin.org/status/302")
    print(res.headers)
    print(res.status_code)
    assert "Location" not in res.headers
    res = post(url="http://httpbin.org/status/302", redirect=False)
    print(res.headers)
    print(res.status_code)
    assert "Location" in res.headers


def test_session():
    # session客户端测试
    session_client = session()
    res = session_client.get(url="http://127.0.0.1/cookie2.php")
    print(res.text)
    res = session_client.get(url="http://127.0.0.1/cookie.php")
    print(res.headers)
    print(res.text)
    res = session_client.get(url="http://127.0.0.1/cookie2.php")
    print(res.text)
    res = session_client.get(url="http://127.0.0.1/cookie2.php")
    print(res.text)


def test_file():
    # 上传文件测试
    with open("1.png", "rb") as f:
        data = f.read()
    res = post(url="http://httpbin.org/post", fields={'form_attri_name': ('example.txt', data, 'MIME')}, proxy="http://127.0.0.1:8080")
    print(res.text)


if __name__ == "__main__":
    test_get()
    test_cookies()
    test_headers()
    test_post()
    test_json()
    test_proxy()
    test_redirect()
    test_session()
    test_file()
