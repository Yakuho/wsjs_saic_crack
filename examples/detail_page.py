"""商标综合查询tab 详情页example"""
from pprint import pprint

from lxml import html

from examples import _BaseExample

API = "http://120.78.76.198:8000/trademark/detail"


class DetailPageExample(_BaseExample):
    def __init__(self, tid: str, *args, **kwargs):
        super(DetailPageExample, self).__init__(*args, **kwargs)
        self.tid = tid

    def detail_page(self):
        """商标详情页"""
        url = "http://wsjs.saic.gov.cn/txnDetail.do"

        request_args = {
            "request:tid": self.tid,
        }

        response = self._request(url=url, request_args=request_args, api=API)

        # 提取数据
        if rb"infoComplate = '1'" in response.content:
            html_doc = html.fromstring(response.content)
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

        request_args = {
            "request:tid": self.tid,
        }

        response = self._request(url=url, request_args=request_args, api=API)

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
