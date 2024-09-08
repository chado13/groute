from typing import TypedDict

class SpotData(TypedDict):
    name: str
    address: str
    lat: float
    lag: float
    category: str


class ResultSpotData(SpotData):
    order: int