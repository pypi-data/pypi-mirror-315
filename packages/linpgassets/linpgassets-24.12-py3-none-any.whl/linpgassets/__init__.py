from json import load as JSON_LOAD
from os import path as PATH
from typing import Final

# 引擎素材路径
IMAGE_PATH: Final[str] = PATH.join(PATH.dirname(__file__), "image")

# 引擎数据库路径
DATABASE_PATH: Final[str] = PATH.join(PATH.dirname(__file__), "config", "database.json")


# 获取数据库
def get_database() -> dict[str, dict[str, dict[str, bool]]]:
    with open(DATABASE_PATH, "r", encoding="utf-8") as f:
        return dict(JSON_LOAD(f))
