"""商标综合查询tab 详情页example"""
from pprint import pprint
from urllib import parse

import requests
from lxml import html

API = "http://120.78.76.198:8000/trademark"


class DetailPageExample:
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

    def _request(self, url: str, tid: str) -> requests.Response:
        path = parse.urlparse(url).path

        request_args = {
            "request:tid": tid,
        }

        response = self.session.post(API, json={"path": path, "request_args": request_args})
        json_data = response.json()
        pprint(json_data)

        response = self.session.post(url, **json_data)
        if response.status_code != 200:
            raise Exception(response.status_code)

        return response

    def detail_page(self, tid: str):
        """商标详情页"""
        url = "http://wsjs.saic.gov.cn/txnDetail.do"
        response = self._request(url=url, tid=tid)

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

    def process_page(self, tid: str):
        """商标流程页"""
        url = "http://wsjs.saic.gov.cn/txnDetail2.do"
        response = self._request(url=url, tid=tid)

        # 提取数据
        keys = ("申请/注册号", "业务名称", "环节名称", "结论", "日期")
        for table in html.fromstring(response.content).xpath("//*[@class='lcbg']//table"):
            values = [td.xpath("string()") for td in table.xpath(".//td")]
            print(dict(zip(keys, values)))

    def run(self, tid: str):
        try:
            self.detail_page(tid)
        except Exception as e:
            print(e)

        try:
            self.process_page(tid)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    example = DetailPageExample()
    example.run(tid="TID2019057434B2208C2A7FED13413F699DF629A035310")
