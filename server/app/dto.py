from pydantic import BaseModel, Field
from datetime import datetime
from app.typed import SpotData
from typing import Any

class TripData(BaseModel):
    destination: str = Field(examples=["서울"])
    schedule: list[datetime] | Any
    spots: list[SpotData]| Any
    hotel: SpotData | None| Any
    arrival: SpotData | None| Any
    depart: SpotData | None| Any
    transport: str


class AssistantResponse(BaseModel):
    assistant_id: str
    thread_id: str
