from typing import Any

import requests
from requests.packages.urllib3 import ssl
import re
from config import config

BASIC_PARAMS = {
    "MobileOS": "ETC",
    "MobileApp": "AppTest",
    "_type": "json",
    "serviceKey": config.tour_api_service_key,
}
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "User-Agent",
}
BASE_URL = "https://apis.data.go.kr/B551011/KorService1"
CATEGORY = {
    "관광지": 12,
    "문화시설": 14,
    "축제공연행사": 15,
    "여행코스": 25,
    "레포츠": 28,
    "숙박": 32,
    "쇼핑": 38,
    "음식점": 39,
}


def fetch_all_area_code() -> list[dict[str, Any]]:
    path = "/areaCode1"
    params = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "_type": "json",
        "serviceKey": config.tour_api_key,
    }
    url = BASE_URL + path
    session = requests.session()
    session.mount("https://", TLSAdapter())
    res = session.get(url, params=params)
    return res.json()["response"]["body"]["items"]["item"]


def fetch_area_spot_list(area_code: str, num_of_rows: int) -> list[dict[str, Any]]:
    path = "/areaBasedList1"
    url = BASE_URL + path
    session = requests.session()
    session.mount("https://", TLSAdapter())
    result = []
    page = 0
    while True:
        page += 1
        params = {
            "MobileOS": "ETC",
            "MobileApp": "AppTest",
            "_type": "json",
            "serviceKey": config.tour_api_key,
            "areaCode": area_code,
            "numOfRows": str(num_of_rows),
            "pageNo": str(page),
            "listYN": "Y",
            "arrange": "A",  # 제목순
        }
        res = session.get(url, params=params)
        try:
            data = res.json()["response"]["body"]["items"]["item"]
        except Exception as e:
            print(e)
            return []
        result += data
        if len(data) < num_of_rows:
            break
    return result


def fetch_area_by_location(
    map_x: float, map_y: float, redius: int, content_type: str | None
):
    content = None
    if content_type:
        categories = content_type.split(">")
        for category in categories:
            keyword = category.split(",")[0]
            pattern = re.compile(rf"{keyword.strip()}")
            for key in CATEGORY.keys():
                if re.search(pattern, key):
                    content = key
    category_id = CATEGORY.get(content) if content else None
    params = {
        "mapX": map_x,
        "mapY": map_y,
        "radius": redius,
        "numOfRows": 10,
        "contentTypeId": category_id,
        **BASIC_PARAMS,
    }
    path = "/locationBasedList1"
    url = BASE_URL + path
    session = requests.session()
    session.mount("https://", TLSAdapter())
    res = session.get(url, params=params)
    try:
        data = res.json()["response"]["body"]["items"]["item"]
    except TypeError:
        return None
    return data


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
