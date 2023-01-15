import os

from dotenv import load_dotenv
from fastapi import FastAPI

from loader.router import API_ROUTERS
from loader.tmp import init_tmp_dir


class Config:
    port: int
    mode: str = 'dev'

    def __init__(self):
        load_dotenv()
        self.port = int(os.getenv('SERVER_PORT', '8000'))
        self.mode = os.getenv('SERVER_MODE', 'dev')

def enroll_routers(app: FastAPI) -> FastAPI:
    for router in API_ROUTERS:
        app.include_router(router)
    return app

def init_app() -> FastAPI:
    init_tmp_dir()
    return enroll_routers(FastAPI())
