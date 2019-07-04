"""商品/服务项目tab example"""
from urllib import parse

import execjs.runtime_names
import requests
from lxml import html

from js import get_crack_js

ctx = execjs.get(execjs.runtime_names.Node).compile(get_crack_js())


class GoodsServiceExample:
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

    def run(self):
        url = "http://wsjs.saic.gov.cn/txnGoodsService01.ajax"
        path = parse.urlparse(url).path

        page = 1
        page_size = 15

        request_args = {
            "request:nc": "",  # 国际分类
            # "request:ncs": "",  # 类似群
            "request:goodstype": "",  # 商品类型
            "request:fiveparty": "",  # 五方
            # "request:fiveparty_y": "1",  # 是五方
            # "request:fiveparty_n": "0",  # 不是五方
            "request:goodssername": "",  # 商品名称
            "request:goodcode": "",  # 商品编码

            "attribute-node:record_cache-flag": "false",
            "attribute-node:record_page": page,
            "attribute-node:record_page-row": page_size,
            "attribute-node:record_sort-column": "",
            "attribute-node:record_start-row": (page - 1) * page_size + 1,
        }
        string = "&".join(f"{k}={v}" for k, v in request_args.items())

        # 更新cookie
        self.session.cookies.update(ctx.call("get_cookies"))

        # 加密请求参数
        mm = ctx.call("get_MmEwMD", path)
        c1k5 = ctx.call("get_c1K5tw0w6", string, mm, 5)

        params = {"MmEwMD": mm}
        data = {"c1K5tw0w6_": c1k5}

        response = self.session.post(url, params=params, data=data)
        if response.status_code != 200:
            raise Exception(response.content.decode())

        # 提取数据
        html_doc = html.fromstring(response.content)
        for record in html_doc.xpath("//record"):
            print({
                "国际分类": (record.xpath("nc/text()") or [None])[0],
                "类似群": (record.xpath("ncs/text()") or [None])[0],
                "商品/服务项目": (record.xpath("goodssername/text()") or [None])[0],
                "五方": (record.xpath("fiveparty/text()") or [None])[0],
                "商品编码": (record.xpath("goodcode/text()") or [None])[0],
                "商品类型": (record.xpath("goodstype/text()") or [None])[0],
            })


if __name__ == "__main__":
    example = GoodsServiceExample()
    example.run()
