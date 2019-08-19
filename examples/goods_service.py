"""商品/服务项目tab example"""
from lxml import html

from examples import _BaseExample

API = "http://120.78.76.198:8000/trademark/goods_service"


class GoodsServiceExample(_BaseExample):

    def run(self):
        url = "http://wsjs.saic.gov.cn/txnGoodsService01.ajax"

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

        response = self._request(url=url, request_args=request_args, api=API)

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
