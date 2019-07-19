"""商标综合查询tab 详情页example"""
from pprint import pprint
from urllib import parse

import requests
from lxml import html

from common.api import online_encrypt
from common.js import ctx
from examples import _BaseExample

API = "http://120.78.76.198:8000/trademark/detail"


class DetailPageExample(_BaseExample):
    def __init__(self, tid: str, *args, **kwargs):
        super(DetailPageExample, self).__init__(*args, **kwargs)
        self.tid = tid

    @staticmethod
    def local_encrypt(path: str, request_args: dict) -> dict:
        """调用本地js上下文加密"""
        string = "&".join(f"{k}={v}" for k, v in request_args.items())

        cookies = ctx.call("get_cookies")

        y7b = ctx.call("get_y7bRbp", path, string)
        c1k5 = ctx.call("get_c1K5tw0w6", string, y7b, 2)
        params = {"y7bRbp": y7b, "c1K5tw0w6_": c1k5}

        return {
            "cookies": cookies,
            "params": params,
        }

    def _request(self, url: str) -> requests.Response:
        path = parse.urlparse(url).path

        request_args = {
            "request:tid": self.tid,
        }

        # 本地加密 TODO 已失效
        # kwargs = self.local_encrypt(path=path, request_args=request_args)

        # 在线加密
        kwargs = online_encrypt(url=API, path=path, request_args=request_args)

        response = self.session.post(url, **kwargs)
        if response.status_code != 200:
            raise Exception(response.status_code)

        return response

    def detail_page(self):
        """商标详情页"""
        url = "http://wsjs.saic.gov.cn/txnDetail.do"
        response = self._request(url)

        # 提取数据
        html_doc = html.fromstring(response.content)
        if not all((not v or v == "null") for v in html_doc.xpath("//*[@id='detailParameter']/input/@value")):
            page_data = {
                "商标图片": html_doc.xpath("//*[@id='tmImage']/@img_src")[0],
                "商品/服务": "".join(html_doc.xpath("//*[@class='info']")[0].text.split()),
                "类似群": [dict(zip(["类似群", "商品名称"], tr.xpath("td/text()"))) for tr in html_doc.xpath("//*[@id='list_box']/table/tr")[1:]],
            }
            for tr in html_doc.xpath("//*[@id='tmContent']/table[2]/tr")[:-1]:
                td_list = tr.xpath("td")
                for index in range(0, len(td_list), 2):
                    key = td_list[index].xpath("span/text()")
                    if key:
                        key = key[0]
                        value = (td_list[index + 1].xpath("text()") or [""])[0]
                        page_data[key] = value.strip()
            pprint(page_data)
        else:
            print("商标详情无数据，可能是商标正等待受理，暂无法查询详细信息。")

    def process_page(self):
        """商标流程页"""
        url = "http://wsjs.saic.gov.cn/txnDetail2.do"
        response = self._request(url=url)

        # 提取数据
        keys = ("申请/注册号", "业务名称", "环节名称", "结论", "日期")
        for table in html.fromstring(response.content).xpath("//*[@class='lcbg']//table"):
            values = [td.xpath("string()") for td in table.xpath(".//td")]
            print(dict(zip(keys, values)))

    def run(self):
        try:
            self.detail_page()
        except Exception as e:
            print(e)

        try:
            self.process_page()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    example = DetailPageExample(tid="TID2019057434B2208C2A7FED13413F699DF629A035310")
    example.run()
