import requests


class _BaseExample:
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wsjs.saic.gov.cn",
            "Origin": "http://wsjs.saic.gov.cn",
            "Referer": "http://wsjs.saic.gov.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        # self.session.proxies = TODO 配置你的代理
