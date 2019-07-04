import os


def get_crack_js():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(dir_path, "crack.js")

    with open(file_path, encoding="utf-8") as f:
        return f.read()
