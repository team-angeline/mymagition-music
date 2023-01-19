from flask import Flask

from functions.pcfl.api import pcfl_view
from utils.file import TmpFileStorage

app = Flask(__name__)

# API 끼워넣기
app.register_blueprint(pcfl_view, url_prefix='/pcfl')

if __name__ == '__main__':
    TmpFileStorage.init_tmpfile('tmp')
    app.run(host='0.0.0.0', port=5000, debug=True)
