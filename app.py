import os
from dotenv import load_dotenv
from flask import Flask

from functions.pcfl.api import pcfl_view
from utils.file import TmpFileStorage

app = Flask(__name__)

# API 끼워넣기
app.register_blueprint(pcfl_view, url_prefix='/pcfl')

# TMP 파일 설정
TmpFileStorage.init_tmpfile('tmp')

if __name__ == '__main__':
    if os.path.isfile('.env'):
        load_dotenv()

    mode = os.getenv('SERVER_MODE', 'dev')
    port = int(os.getenv('SERVER_PORT', '5000'))

    if mode not in ('dev', 'prod'):
        raise ValueError("Select mode (dev or prod)")

    app.run(host='0.0.0.0',
            port=os.getenv('SERVER_PORT', 5000),
            debug=(mode == 'dev'))
