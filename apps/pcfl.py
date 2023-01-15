from fastapi import APIRouter, status

router = APIRouter(prefix='/pcfl',
                   responses = {404: {'msg': 'Not Found'}})

@router.post(path='', status_code=status.HTTP_200_OK)
def run_pcfl():
    return {'msg': 'hello world'}
