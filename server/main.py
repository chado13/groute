from fastapi import APIRouter, FastAPI, Body, Depends

from pydantic import BaseModel, Field
from typing import Annotated
from server.deps import get_assistant

router = APIRouter()

app = FastAPI()

class TripData(BaseModel):
    destination: str = Field(examples=["서울"])
    period: str
    locations: list[str]
    hotel: str | None
    arrival: str | None
    depart: str | None
    transportation: str

class AssistantResponse(BaseModel):
    assistant_id: str
    thread_id: str

@app.get("/groute/assistant/{user_id}")
def get(user_id: int, assistant = Depends(get_assistant)) -> AssistantResponse:
    return AssistantResponse(assistant_id=assistant.assistant_id, thread_id=assistant.thread_id)

@app.post("/groute/{thread_id}")
def send_message(thread_id: str, data: Annotated[TripData, Body], assistant = Depends(get_assistant)):
    content = (
        f"{data.destination}의 {",".join(data.locations)}을  {data.period} 일정으로 여행할 예정입니다. "
        f"{data.arrival}에 도착하여 일정을 시작하여 {data.depart}에서 돌아갈 예정입니다."
        f"여행일정 내내 {data.hotel}에서 숙박할 예정이고 주요 이동수단으로는 {data.transportation}를 이용할 예정입니다."
    )
    assistant.send_message(content)
    message = assistant.run_assistant()
    return message    