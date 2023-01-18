from typing import Tuple

from werkzeug.datastructures import FileStorage


def _validate_interval(form_interval: str | None) -> Tuple[float | None, str | None]:
    if not form_interval:
        return None, 'interval을 설정해 주세요'
    try:
        interval = float(form_interval)
    except ValueError:
        return None, 'interval은 실수여야 합니다.'

    if not (0.1 <= interval < 0.6):
        return None, 'interval은 0.1이상 0.6 미만이어야 합니다.'

    return interval, None

def _validate_midi(form_midi: FileStorage | None) -> str | None:
    if not form_midi:
        return '미디파일을 추가해 주세요'

    ext = form_midi.filename.split('.')[-1]
    if ext not in {'mid', 'midi'}:
        return '미디파일만 추가할 수 있습니다.'

    return None

def validate(form_interval: str | None, form_midi: FileStorage | None) \
        -> Tuple[str | None, FileStorage | None, str | None]:
    interval, err = _validate_interval(form_interval)
    if err:
        return None, None, err
    err = _validate_midi(form_midi)
    if err:
        return None, None, err
    return interval, form_midi, None