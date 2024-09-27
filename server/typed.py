from typing import TypedDict
import datetime

class SpotData(TypedDict):
    name: str
    address: str
    lat: float
    lag: float
    category: str


class ResultSpotData(SpotData):
    order: int


class ResultResponse(TypedDict):
    start_date: datetime.date
    end_date: datetime.date
    period: int
    spots: list[ResultSpotData]
    