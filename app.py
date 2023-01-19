import sys

from flask import Flask

from functions.pcfl.api import pcfl_view
from utils.file import TmpFileStorage

app = Flask(__name__)

# API 끼워넣기
app.register_blueprint(pcfl_view, url_prefix='/pcfl')

# TMP 파일 설정
TmpFileStorage.init_tmpfile('tmp')

if __name__ == '__main__':
    # DEV용
    app.run(host='0.0.0.0', port=5000, debug=True)