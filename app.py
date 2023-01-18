import os.path
import random

from flask import Flask, request, Response

from functions.pcfl.validations import validate as pcfl_validate
from utils.file import TmpFileStorage

from submodules.pcfl.pcfl import make_config as make_pcfl_config, pcfl

app = Flask(__name__)

@app.post('/pcfl')
def api_pcfl():
    form_interval, form_midi = \
        request.form.get('interval', None), request.files.get('file', None)
    interval, midi, err = pcfl_validate(form_interval, form_midi)

    # 임시파일 생성
    tmp_obj = TmpFileStorage(midi)
    tmp_obj.save()

    # config 세팅
    input_file = str(tmp_obj)
    output_file = f'{TmpFileStorage.tmp_root}/{random.randint(1, abs(hash(midi.filename)))}-output.mid'
    pcfl_config = make_pcfl_config(input_file, output_file, interval)

    try:
        pcfl(pcfl_config)
    except Exception:
        return {'msg': 'got error'}, 400

    if not os.path.isfile(output_file):
        return {'msg': '결과 파일을 가져오는 데 실패했습니다.'}, 400

    with open(output_file, 'rb') as of:
        data = of.read(10**5)
    response = Response(response=data,
                        mimetype='audio/mid',
                        content_type='application/octet-stream')
    response.headers["Content-Disposition"] = f"attachment; filename={midi.filename}"

    # 파일 전부 삭제
    os.remove(output_file)
    tmp_obj.remove()

    return response


if __name__ == '__main__':
    TmpFileStorage.init_tmpfile('tmp')
    app.run(host='0.0.0.0', port=5000, debug=True)