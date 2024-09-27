from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from routes import groute

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groute.router)
