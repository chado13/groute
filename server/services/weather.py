from config import config
import orjson
from typing import Any

from collections.abc import AsyncGenerator, Awaitable, Callable, Mapping
import aiohttp
import asyncio
from contextlib import asynccontextmanager
import datetime
import requests
from requests.packages.urllib3 import ssl
import polars as pl
import re

REGION_ID = {
    "서울, 인천, 경기도": "11B00000",
    "강원도영서": "11D10000",
    "강원도영동": "11D20000",
    "대전, 세종, 충청남도": "11C20000",
    "충청북도": "11C10000",
    "광주, 전라남도": "11F20000",
    "전북자치도": "11F10000",
    "대구, 경상북도": "11H10000",
    "부산, 울산, 경상남도": "11H20000",
    "제주도": "11G00000",
}

WEATHER_CODE = {
    "맑음": "10",
    "구름많음": "30",
    "흐림": "40",
    "흐리고비": "41",
    "구름많고비": "31",
    "맑고눈": "13",
    "맑고비나눈": "12",
    "맑고눈": "13",
    "맑고소나기": "14",
    "구름많고눈": "32",
    "구름많고비나눈": "33",
    "구름많고소나기": "34",
    "흐리고비나눈": "42",
    "흐리고비나눈": "43",
    "흐리고눈": "42",
    "흐리고소나기": "44",
}
with open("./resources/region.json", "r") as f:
    REGION = orjson.loads(f.read())


@asynccontextmanager
async def request(
    method: str,
    url: aiohttp.typedefs.StrOrURL,
    headers: aiohttp.typedefs.LooseHeaders | None = None,
    params: Mapping[str, str] | None = None,
    data: Any = None,
    json: Any = None,
    timeout: float | None = 5,
    **kwargs: Any,
) -> AsyncGenerator[aiohttp.ClientResponse, None]:
    try:
        client = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout))
        resp = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            **kwargs,
        )
        yield resp
    finally:
        await client.close()


def fetch_weathers(
    location: str,
    x: int,
    y: int,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[str | None]:
    now = datetime.datetime.now()
    middle_term_df = fetch_middle_term_weathers(location=location, now=now)
    short_term_df = fetch_short_term_weathers(now, x, y)
    data = (
        pl.concat([short_term_df, middle_term_df], how="vertical_relaxed")
        .sort("key")
        .unique(subset="key", keep="first")
        .to_dicts()
    )
    data = {each["key"]: each["value"] for each in data}
    i = 0
    res = []
    while True:
        date = start_date + datetime.timedelta(days=i)
        item = data.get(date)
        res.append(item)
        i += 1
        if date == end_date:
            break
    return res


def fetch_middle_term_weathers(location: str, now: datetime.datetime):
    """중기 일기 예보
    dt로부터 3일 이후부터 10일 후 까지의 일기를 예보
    """
    region = None
    for key, value in REGION.items():
        if location in value:
            region = key
    region_id = REGION_ID.get(region)
    dt = (
        now.strftime("%Y%m%d") + "0600"
        if now.time() < datetime.time(18, 0)
        else now.strftime("%Y%m%d") + "1800"
    )
    params = {
        "ServiceKey": config.weather_api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "json",
        "regId": region_id,
        "tmFc": dt,
    }
    url = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
    session = requests.session()
    session.mount("https://", TLSAdapter())
    res = session.get(url, params=params)
    data = res.json()["response"]["body"]["items"]["item"]
    res = []
    for key, value in data[0].items():
        if "wf" in key and "Pm" not in key:
            delta = re.search(r"\d", key).group()
            date = now + datetime.timedelta(days=int(delta))
            v = value.strip().replace(" ", "")
            value = WEATHER_CODE.get(v, "00")
            res.append({"key": date.date(), "value": value})
    return pl.DataFrame(res)


def fetch_short_term_weathers(now: datetime.datetime, x: int, y: int) -> pl.DataFrame:
    def _process(df: pl.DataFrame) -> pl.DataFrame:
        data = (
            df.explode(columns=["category", "fcstValue"])
            .pivot(values="fcstValue", index="key", columns="category")
            .with_columns(value=pl.col("SKY") + pl.col("PTY"))
        )
        return data.select(["key", "value"])

    dt = now.strftime("%Y%m%d")
    base_time = get_base_time(now)
    params = {
        "ServiceKey": config.weather_api_key,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "json",
        "base_date": dt,
        "base_time": base_time,
        "nx": x,
        "ny": y,
    }
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    session = requests.session()
    session.mount("https://", TLSAdapter())
    res = session.get(url, params=params)
    items = res.json()["response"]["body"]["items"]["item"]
    df = pl.DataFrame(items)
    if df.is_empty():
        return df
    dates = (
        df.unique(subset=["fcstDate"])
        .with_columns(key=pl.col("fcstDate") + pl.col("fcstTime"))
        .select("key")
        .to_series()
        .to_list()
    )
    df = (
        df.with_columns(key=pl.col("fcstDate") + pl.col("fcstTime"))
        .group_by("key")
        .agg([pl.col("category"), pl.col("fcstValue")])
        .filter(pl.col("key").is_in(dates))
        .group_by("key")
        .map_groups(lambda df: _process(df))
    )
    return df.with_columns(pl.col("key").str.strptime(pl.Datetime, "%Y%m%d%H%M")).cast(
        {"key": pl.Date}
    )


def get_base_time(now: datetime.datetime) -> str:
    now_time = now.time()
    if now_time > datetime.time(2, 10) and now_time < datetime.time(5, 10):
        return "0200"
    elif now_time > datetime.time(5, 10) and now_time < datetime.time(8, 10):
        return "0500"
    elif now_time > datetime.time(8, 10) and now_time < datetime.time(11, 10):
        return "0800"
    elif now_time > datetime.time(11, 10) and now_time < datetime.time(14, 10):
        return "1100"
    elif now_time > datetime.time(14, 10) and now_time < datetime.time(17, 10):
        return "1400"
    elif now_time > datetime.time(17, 10) and now_time < datetime.time(20, 10):
        return "1700"
    elif now_time > datetime.time(20, 10) and now_time < datetime.time(23, 10):
        return "2000"
    else:
        return "2300"


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
