import multiprocessing
import os

def get_worker_size():
    n = multiprocessing.cpu_count()
    return 1 if n == 1 else n // 2

port = os.getenv('SERVER_PORT', '5000')

bind = f'0.0.0.0:{port}'
workers = get_worker_size()
errorlog = 'log/error.log'
accesslog = 'log/access.log'
