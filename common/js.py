import os
from typing import Dict, Union
from urllib import parse

import execjs.runtime_names


def _get_crack_js() -> str:
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(project_path, "js", "crack.js")

    with open(file_path, encoding="utf-8") as f:
        return f.read()


ctx: execjs.ExternalRuntime.Context = execjs.get(execjs.runtime_names.Node).compile(_get_crack_js())


def local_encrypt(path: str, request_args: Dict[str, Union[str, int]]) -> dict:
    string = "&".join(f"{k}={parse.quote(str(v))}" for k, v in request_args.items())

    if path == "/txnGoodsService01.ajax":
        mm = ctx.call("get_MmEwMD", path)
        c1k5 = ctx.call("get_c1K5tw0w6", string, mm, 5)
        params = {"MmEwMD": mm}
        data = {"c1K5tw0w6_": c1k5}

    elif path == "/txnRead01.do":
        y7b = ctx.call("get_y7bRbp", path, "")
        c1k5 = ctx.call("get_c1K5tw0w6", string, y7b, 7)
        params = {"y7bRbp": y7b}
        data = {"c1K5tw0w6_": c1k5}

    elif path == "/txnRead02.ajax":
        mm = ctx.call("get_MmEwMD", path)
        c1k5 = ctx.call("get_c1K5tw0w6", string, mm, 5)
        params = {"MmEwMD": mm}
        data = {"c1K5tw0w6_": c1k5}

    elif path in ("/txnDetail.do", "/txnDetail2.do"):
        y7b = ctx.call("get_y7bRbp", path, string)
        c1k5 = ctx.call("get_c1K5tw0w6", string, y7b, 2)
        params = {"y7bRbp": y7b, "c1K5tw0w6_": c1k5}
        data = {}

    else:
        raise Exception(f"invalid path: {path}")

    return {
        "cookies": ctx.call("get_cookies"),
        "params": params,
        "data": data,
    }
