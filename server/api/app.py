from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from api.config import config
from api.routes import groute

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groute.router)

# Vercel에서 사용할 수 있도록 핸들러 추가
def handler(request):
    return app.handle_request(request)

