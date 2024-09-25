from pydantic import BaseModel, Field
from datetime import datetime
from api.typed import SpotData
from typing import Any

class TripData(BaseModel):
    destination: str = Field(examples=["서울"])
    start: datetime | Any
    end: datetime | Any
    spots: list[SpotData]| Any
    hotel: SpotData | None
    arrival: SpotData | None| Any
    depart: SpotData | None| Any
    transport: str | None


class AssistantResponse(BaseModel):
    assistant_id: str
    thread_id: str
