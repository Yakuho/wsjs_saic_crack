from urllib import parse

import requests

from common.api import online_encrypt
from common.js import local_encrypt


class _BaseExample:
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wsjs.saic.gov.cn",
            "Origin": "http://wsjs.saic.gov.cn",
            "Referer": "http://wsjs.saic.gov.cn/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        # self.session.proxies = dict.fromkeys(("http", "https"), "TODO 配置你的代理")

    def _request(self, url: str, request_args: dict, *, method="POST", api: str = None) -> requests.Response:
        path = parse.urlparse(url).path

        if not api:
            kwargs = local_encrypt(path=path, request_args=request_args)  # 本地加密 TODO 已失效
        else:
            kwargs = online_encrypt(api=api, path=path, request_args=request_args)  # 在线加密

        response = self.session.request(method=method, url=url, **kwargs)
        if response.status_code != 200:
            raise Exception(response.status_code)

        return response
