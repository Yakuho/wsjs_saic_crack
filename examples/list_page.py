"""商标综合查询tab 列表页example"""
import hashlib
from urllib import parse

from lxml import html

from examples import _BaseExample

API = "http://120.78.76.198:8000/trademark/list"


class ListPageExample(_BaseExample):

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
        request_args["request:md5"] = self.get_md5(request_args)

        response = self._request(url=url, request_args=request_args, api=API)

        # 提取后续请求所需数据
        html_doc = html.fromstring(response.content)
        html_args = {
            "request:mi": html_doc.xpath("//input[@name='request:mi']/@value")[0],
            "request:tlong": html_doc.xpath("//input[@name='request:tlong']/@value")[0],
        }

        print(html_args)
        return html_args

    def step2(self, keyword: str, html_args: dict):
        """请求数据接口"""
        url = "http://wsjs.saic.gov.cn/txnRead02.ajax"

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

        response = self._request(url=url, request_args=request_args, api=API)

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
