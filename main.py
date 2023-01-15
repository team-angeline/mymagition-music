from fastapi import FastAPI
import uvicorn

from loader.boot import Config, init_app

app: FastAPI = init_app()

if __name__ == '__main__':
    config: Config = Config()

    if config.mode == 'dev':
        uvicorn.run('main:app', port=config.port, log_level='info')
    elif config.mode == 'prod':
        app.docs_url = app.redoc_url = None
        uvicorn.run('main:app', port=config.port)


