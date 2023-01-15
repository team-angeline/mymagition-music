import os
from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, Form, HTTPException
from starlette.background import BackgroundTasks
from starlette.responses import StreamingResponse

from utils.id import generate_randomize_id, generate_file_root

from submodules.pcfl.pcfl import pcfl
from submodules.pcfl.pcfl import make_config as make_pcfl_config

router = APIRouter(prefix='/pcfl',
                   responses = {
                       404: {'detail': 'Not Found'},
                       422: {'detail': '요청값이 알맞지 않습니다.'}
                   })

def validate_interval(interval: float) -> bool:
    """
    Interval의 범위는  0.01 ~ 0.5
    :param interval: CC64 데이터 사이의 간격
    :return: Validate 통과 여부
    """
    return 0.01 <= interval < 0.5

async def write_tmp(root: str, file: UploadFile) -> None:
    """
    TMP 파일 생성

    :param root: 저장될 루트
    :param file: Client로부터 받아온 파일
    :return: None
    """
    with open(root, 'wb') as f:
        f.write(await file.read())

def make_input_output_root(client_id):
    """
    Client ID를 기반한 예상 I/O 파일 루트 생성

    :param client_id: client id
    :return:
    """
    prefix = generate_file_root(client_id, 'pcfl')
    return f'{prefix}-input.mid', f'{prefix}-output.mid'

def run_pcfl(input_root, output_root, interval) -> Optional[str]:
    """
    PCFL 실행

    :param input_root: input root
    :param output_root: output root
    :param interval: interval
    :return: 에러 메세지, 성공일 경우 None
    """
    config = make_pcfl_config(input_root, output_root, interval)
    try:
        pcfl(config)
    except ValueError:
        return '트랙이 비어있습니디.'
    except (RuntimeError, Exception):
        return '교정하는 데 실패했습니다. 미디파일을 다시 한번 확인해 주세요.'
    else:
        os.unlink(input_root)
        return None

@router.post(path='', status_code=status.HTTP_200_OK)
async def api(background_tasks: BackgroundTasks,
              interval: float = Form(),
              file: UploadFile = File(...)):

    # validate interval
    if not validate_interval(interval):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Interval의 범위는 0.01이상 0.5 미만 입니다.')

    # Setting TMP File Roots
    input_root, output_root = \
        make_input_output_root(
            generate_randomize_id())

    # Write input data
    await write_tmp(input_root, file)

    # Run PCFL and remove input_file
    err_msg: Optional[str] = run_pcfl(input_root, output_root, interval)
    if err_msg:
        # 에러 발생
        raise HTTPException(status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                            detail=err_msg)

    # Make Response
    file_body = open(output_root, mode='rb')
    response = StreamingResponse(file_body, media_type='audio/mid')
    response.headers['Content-Disposition'] = "attachment; filename=output.mid"

    # Background에서 해당 파일 처리
    background_tasks.add_task(os.unlink, output_root)

    # Response
    return response
