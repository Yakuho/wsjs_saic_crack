import time
from typing import Dict, Union

import requests


def online_encrypt(url: str, path: str, request_args: Dict[str, Union[str, int]], **kwargs) -> dict:
    """调用api加密
    TODO 接口限速每秒1个请求，超出返回503
    """
    time.sleep(1)  # 防止请求过快返回503

    response = requests.post(url, json=dict(path=path, request_args=request_args), **kwargs)
    if response.status_code == 503:
        raise Exception("接口流量控制，服务暂不可用")

    json_data = response.json()
    return json_data
