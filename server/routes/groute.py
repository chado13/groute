from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter
from fastapi import Body, Query

from dto import TripData
from typed import ResultSpotData, ResultResponse
from services import route as service
from services import tourapi
from services.weather import fetch_weathers
from zoneinfo import ZoneInfo
import pytz

router = APIRouter()


@router.post("/groute/route")
async def get_route(data: Annotated[TripData, Body]) -> dict[str, Any]:
    start_date = (
        datetime.strptime(data.start, "%Y-%m-%dT%H:%M:%S.%fZ")
        .replace(tzinfo=pytz.utc)
        .astimezone(tz=ZoneInfo("Asia/Seoul"))
        .date()
    )
    end_date = (
        datetime.strptime(data.end, "%Y-%m-%dT%H:%M:%S.%fZ")
        .replace(tzinfo=pytz.utc)
        .astimezone(tz=ZoneInfo("Asia/Seoul"))
        .date()
    )
    res: list[ResultSpotData] = service.search(data, start_date, end_date)
    days = (start_date - datetime.now().date()).days
    if days > 10:
        weather = [None for i in range(0, days)]
    else:
        x = float(data.spots[0]["lat"])
        y = float(data.spots[0]["lng"])
        weathers = fetch_weathers(
            data.destination, int(x), int(y), start_date, end_date
        )
    response: ResultResponse = {
        "destination": data.destination,
        "start_date": start_date,
        "end_date": end_date,
        "period": (end_date - start_date).days + 1,
        "spots": res,
        "weathers": weathers,
    }
    return response


@router.get("/groute/places")
def fetch_places(
    lng: float, lat: float, redius: int, content_type: str | None = Query(default=None)
) -> list[dict[str, Any]]:
    res = tourapi.fetch_area_by_location(lng, lat, redius, content_type)
    if not res:
        return []
    return [
        {
            "name": item["title"],
            "address": item["addr1"],
            "content_id": item["contentid"],
            "content_type_id": item["contenttypeid"],
            "dist": item["dist"],
            "lat": item["mapy"],
            "lng": item["mapx"],
        }
        for item in res
    ]
