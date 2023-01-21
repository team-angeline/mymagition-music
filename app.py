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
    # 개발용
    # 배포용은 gunicorn.conf.py로
    if os.path.isfile('.env'):
        load_dotenv()
    port = int(os.getenv('SERVER_PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
