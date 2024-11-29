import pandas as pd
import json
from PIL import Image
from converter.exceptions import UNKNOWN_ERROR
import os

# flake8: noqa: F401
import pillow_avif


def type_checker(path: str):
    extension = path.split(".")[-1]
    return extension


def path_devider(long_path: str):
    if "{" not in long_path:
        return list(map(str, long_path.split(" ")))
    paths = list(map(str, long_path.split("} ")))
    paths = [x.replace("{", "").replace("}", "") for x in paths]
    return paths


def convert_docs(path: str, result_type: str):
    type = type_checker(path)
    if type in ["xlsx", "xls"]:
        data = pd.read_excel(path)
    elif type == "csv":
        try:
            data = pd.read_csv(path)
        except:
            data = pd.read_csv(path, encoding="cp1252")
    elif type == "json":
        data = pd.read_json(path)
    else:
        raise UNKNOWN_ERROR
    try:
        if not os.path.isdir("/".join(path.split("/")[0:-1]) + f"/{result_type}"):
            os.makedirs("/".join(path.split("/")[0:-1]) + f"/{result_type}")
    except:
        raise UNKNOWN_ERROR
    save_path = (
        "/".join(path.split("/")[0:-1])
        + f"/{result_type}/{".".join(path.split("/")[-1].split(".")[0:-1])}.{result_type}"
    )
    if result_type == "json":
        result = json.loads(data.to_json(orient="records"))
        with open(save_path, mode="w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
    elif result_type in ["xlsx", "xls"]:
        data.to_excel(save_path, index=False, engine="openpyxl")
    elif result_type == "csv":
        data.to_csv(save_path, index=False)
    else:
        raise UNKNOWN_ERROR


def convert_image(path: str, result_type: str):
    type = type_checker(path)
    if type == "png":
        img = Image.open(path).convert("RGB")
    elif result_type == "png":
        img = Image.open(path).convert("RGBA")
    else:
        img = Image.open(path)
    save_path = (
        "/".join(path.split("/")[0:-1])
        + f"/{".".join(path.split("/")[-1].split(".")[0:-1])}.{result_type}"
    )
    img.save(save_path, quality=100)
