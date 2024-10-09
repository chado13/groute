from typing import TypedDict
import datetime


class SpotData(TypedDict):
    name: str
    address: str
    lat: float  # x
    lng: float  # y
    category: str


class ResultSpotData(SpotData):
    order: int


class ResultResponse(TypedDict):
    destination: str
    start_date: datetime.date
    end_date: datetime.date
    period: int
    spots: list[ResultSpotData]
    weathers: list[str | None]
