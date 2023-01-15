import uvicorn

from loader.boot import Config, init_app

config: Config = Config()
app, conf = init_app(config)

if __name__ == '__main__':
    uvicorn.run('main:app', **conf)
