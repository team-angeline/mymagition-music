import os.path
import random

from flask import Blueprint, request

from functions.pcfl.validations import validate
from utils.file import TmpFileStorage
from utils.response import make_file_response

from submodules.pcfl.pcfl import make_config, pcfl

pcfl_view = Blueprint('PCFL API', __name__)

@pcfl_view.post('')
def api_pcfl():
    # 데이터 갖고오기
    form_interval = request.form.get('interval', None)
    form_midi = request.files.get('file', None)

    # Check Validate
    interval, midi, err = validate(form_interval, form_midi)
    if err:
        return {'msg': err}, 400

    # 임시파일 생성
    tmp_obj = TmpFileStorage(midi)
    tmp_obj.save(force=True)

    # Setting Config
    input_file = str(tmp_obj)   # PCFL에 돌릴 임시 파일의 루트
    """
    output file의 경우, 같은 이름의 파일 충돌 방지를 위해
    1에서부터 hash값의 랜덤값으로 파일 이름을 결정
    """
    output_file = f'{TmpFileStorage.tmp_root}' \
                  f'/' \
                  f'{random.randint(1, abs(hash(midi.filename)))}' \
                  f'-output.mid'
    pcfl_config = make_config(input_file, output_file, interval)

    try:
        # Run PCFL
        pcfl(pcfl_config)
    except ValueError:
        return {'msg': '미디파일이 비어있어요.'}, 400
    except (RuntimeError, Exception):
        # 미디파일을 아예 읽을 수 없는 경우 Exception을 호출한다.
        return {'msg': 'Midi파일이 깨져있어요.'}, 400

    if not os.path.isfile(output_file):
        # 성공은 했는데 파일을 가져올 수 없음
        return {'msg': '결과 파일을 가져오는 데 실패했습니다.'}, 400

    with open(output_file, 'rb') as of:
        # 미디 데이터 바이너리로 가져오기
        data = of.read(10**5)

    # Response 생성
    response = make_file_response(data, 'audio/mid', midi.filename)

    # 파일 전부 삭제
    if os.path.isfile(output_file):
        os.remove(output_file)
    tmp_obj.remove()

    return response