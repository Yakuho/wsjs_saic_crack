"""商标综合查询tab 列表页example"""
import hashlib
from urllib import parse

from lxml import html

from common.api import online_encrypt
from common.js import ctx
from examples import _BaseExample

API = "http://120.78.76.198:8000/trademark/list"


class ListPageExample(_BaseExample):
    @staticmethod
    def local_encrypt(path: str, request_args: dict) -> dict:
        """调用本地js上下文加密"""

        if path == "/txnRead01.do":
            string = "&".join(f"{k}={v}" for k, v in request_args.items())

            y7b = ctx.call("get_y7bRbp", path, "")
            c1k5 = ctx.call("get_c1K5tw0w6", string, y7b, 7)

            params = {"y7bRbp": y7b}
            data = {"c1K5tw0w6_": c1k5}

        elif path == "/txnRead02.ajax":
            string = "&".join(f"{k}={parse.quote(str(v))}" for k, v in request_args.items())

            mm = ctx.call("get_MmEwMD", path)
            c1k5 = ctx.call("get_c1K5tw0w6", string, mm, 5)

            params = {"MmEwMD": mm}
            data = {"c1K5tw0w6_": c1k5}

        else:
            raise Exception("invalid path")

        cookies = ctx.call("get_cookies")

        return {
            "cookies": cookies,
            "params": params,
            "data": data,
        }

    @staticmethod
    def get_md5(data: dict) -> str:
        """用于列表页的md5加密"""
        salt = "MR2W3O4M5R3O1P7W3E9M0R6N8H"
        keys = ("request:nc", "request:ncs", "request:mn", "request:sn", "request:hnc", "request:hne", "request:imf")
        values = [parse.quote(data.get(key) or "@", safe="@") for key in keys] + [salt]
        message = "-".join(values)
        digest = hashlib.md5(message.encode()).hexdigest()
        return digest

    def step1(self, keyword: str) -> dict:
        """访问html页面获取参数"""
        url = "http://wsjs.saic.gov.cn/txnRead01.do"
        path = parse.urlparse(url).path

        request_args = {
            "locale": "zh_CN",  # 语言
            "request:queryCom": "1",  # 不明
            "request:nc": "",  # 国际分类
            "request:sn": "",  # 申请/注册号
            "request:mn": keyword,  # 商标名称
            "request:hnc": "",  # 申请人名称(中文)
            "request:hne": "",  # 申请人名称(英文)
            "request:md5": None,  # md5签名
        }
        request_args["request:md5"] = ListPageExample.get_md5(request_args)

        # 本地加密 TODO 已失效
        # kwargs = self.local_encrypt(path=path, request_args=request_args)

        # 在线加密
        kwargs = online_encrypt(url=API, path=path, request_args=request_args)
        response = self.session.post(url, **kwargs)

        if response.status_code != 200:
            raise Exception(response.status_code)

        # 解析meta标签(9DhefwqGPrzGxEp9hPaoag)
        meta = html.fromstring(response.content).xpath("//*[@id='9DhefwqGPrzGxEp9hPaoag']")[0].get("content")
        # 得到input隐藏域参数
        input_tags = ctx.call("get_hidden_input", meta)
        html_args = {tag.get("name"): tag.get("value") for tag in html.fromstring(input_tags).xpath("//input")}

        print(html_args)
        return html_args

    def step2(self, keyword: str, html_args: dict):
        """请求数据接口"""
        url = "http://wsjs.saic.gov.cn/txnRead02.ajax"
        path = parse.urlparse(url).path

        page = 1
        page_size = 50

        request_args = {
            "locale": "zh_CN",  # 语言
            "request:queryCom": "1",
            "request:nc": "",  # 国际分类
            "request:sn": "",  # 申请/注册号
            "request:mn": keyword,  # 商标名称
            "request:hnc": "",  # 申请人名称(中文)
            "request:hne": "",  # 申请人名称(英文)

            "request:imf": "",
            "request:maxHint": "",
            "request:ncs": "",
            "request:queryAuto": "",
            "request:queryExp": f"mnoc = {keyword}*",
            "request:queryMode": "",
            "request:queryType": "",
            "request:mi": html_args["request:mi"],
            "request:tlong": html_args["request:tlong"],

            "attribute-node:record_cache-flag": "false",
            "attribute-node:record_page": page,
            "attribute-node:record_page-row": page_size,
            "attribute-node:record_sort-column": "RELEVANCE",
            "attribute-node:record_start-row": (page - 1) * page_size + 1,
        }

        # 本地加密 TODO 已失效
        # kwargs = self.local_encrypt(path=path, request_args=request_args)

        # 在线加密
        kwargs = online_encrypt(url=API, path=path, request_args=request_args)
        response = self.session.post(url, **kwargs)

        if response.status_code != 200:
            raise Exception(response.status_code)

        # 提取数据
        for tag in html.fromstring(response.content).xpath("//record"):
            print({
                "tid": tag.xpath("tid/text()")[0],
                "index": tag.xpath("index/text()")[0],
                "申请/注册号": tag.xpath("tmid/text()")[0],
                "国际分类": tag.xpath("nc/text()")[0],
                "申请日期": tag.xpath("fd/text()")[0],
                "商标名称": tag.xpath("mno/text()")[0],
                "申请人名称": tag.xpath("hnc/text()")[0],
            })

    def run(self, keyword: str):
        html_args = self.step1(keyword)
        self.step2(keyword, html_args)


if __name__ == "__main__":
    example = ListPageExample()
    example.run(keyword="华为")
