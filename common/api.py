import requests


def online_encrypt(url: str, path: str, request_args: dict, **kwargs) -> dict:
    """调用api加密"""
    response = requests.post(url, json=dict(path=path, request_args=request_args), **kwargs)
    json_data = response.json()
    return json_data