import os

import execjs.runtime_names


def _get_crack_js() -> str:
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(project_path, "js", "crack.js")

    with open(file_path, encoding="utf-8") as f:
        return f.read()


ctx: execjs.ExternalRuntime.Context = execjs.get(execjs.runtime_names.Node).compile(_get_crack_js())
