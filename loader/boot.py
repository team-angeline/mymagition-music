import os
from typing import Dict, Optional, Tuple

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from loader.router import API_ROUTERS
from loader.tmp import init_tmp_dir


class Config:
    port: int
    mode: str = 'dev'

    def __init__(self):
        load_dotenv()
        self.port = int(os.getenv('SERVER_PORT', '8000'))
        self.mode = os.getenv('SERVER_MODE', 'dev')

    def to_app_param(self) -> Optional[Dict]:
        if self.mode == 'dev':
            return {
                'debug': True
            }
        elif self.mode == 'prod':
            return {
                'redoc_url': None,
                'openapi_url': None,
                'docs_url': None,
            }
        else:
            return None

    def to_uvicorn_param(self) -> Optional[Dict]:
        if self.mode == 'dev':
            return {
                'port': self.port,
                'log_level': 'info',
            }
        elif self.mode == 'prod':
            return {
                'port': self.port,
            }

def add_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["post"],
        allow_headers=["*"],
    )
    return app

def enroll_routers(app: FastAPI) -> FastAPI:
    for router in API_ROUTERS:
        app.include_router(router)
    return app

def init_app(config: Config) -> Tuple[FastAPI, Dict]:
    init_tmp_dir()
    app_param = config.to_app_param()

    if not app_param:
        raise ValueError()

    app = FastAPI(**app_param)
    add_middlewares(app)
    enroll_routers(app)
    return app, config.to_uvicorn_param()
