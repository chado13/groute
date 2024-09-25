from typing import Any

import requests
from requests.packages.urllib3 import ssl

from api.config import config

BASE_URL = "https://apis.data.go.kr/B551011/KorService1"


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
        data = res.json()["response"]["body"]["items"]["item"]
        result += data
        if len(data) < num_of_rows:
            break
    return result


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
