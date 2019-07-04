"""商标综合查询tab 列表页example"""
import hashlib
from urllib import parse

import execjs.runtime_names
import requests
from lxml import html

from js import get_crack_js

ctx = execjs.get(execjs.runtime_names.Node).compile(get_crack_js())


class ListPageExample:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "wsjs.saic.gov.cn",
            "Origin": "http://wsjs.saic.gov.cn",
            "Referer": "http://wsjs.saic.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

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
        string = "&".join(f"{k}={v}" for k, v in request_args.items())

        # 更新cookie
        self.session.cookies.update(ctx.call("get_cookies"))

        # 加密请求参数
        y7b = ctx.call("get_y7bRbp", path, "")
        c1k5 = ctx.call("get_c1K5tw0w6", string, y7b, 7, True)

        params = {"y7bRbp": y7b}
        data = {"c1K5tw0w6_": c1k5}

        response = self.session.post(url, params=params, data=data)
        if response.status_code != 200:
            raise Exception(response.status_code)

        # 解析meta标签(9DhefwqGPrzGxEp9hPaoag)
        meta = html.fromstring(response.content).xpath("//*[@id='9DhefwqGPrzGxEp9hPaoag']")[0].get("content")
        # 得到input隐藏域参数
        input_tags = ctx.call("get_hidden_input", meta)
        html_args = {tag.get("name"): tag.get("value") for tag in html.fromstring(input_tags).xpath("//input")}

        return html_args

    def step2(self, keyword: str, html_args: dict):
        """请求数据接口"""
        url = "http://wsjs.saic.gov.cn/txnRead02.ajax"
        path = parse.urlparse(url).path

        page = 1
        page_size = 50

        request_args = {
            "request:queryCom": "1",
            "locale": "zh_CN",  # 语言
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
        string = "&".join(f"{k}={parse.quote(str(v))}" for k, v in request_args.items())

        # 更新cookie
        self.session.cookies.update(ctx.call("get_cookies"))

        # 加密请求参数
        mm = ctx.call("get_MmEwMD", path)
        c1k5 = ctx.call("get_c1K5tw0w6", string, mm, 5)

        params = {"MmEwMD": mm}
        data = {"c1K5tw0w6_": c1k5}

        response = self.session.post(url, params=params, data=data)
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
