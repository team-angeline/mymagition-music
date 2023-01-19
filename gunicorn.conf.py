import multiprocessing

def get_worker_size():
    n = multiprocessing.cpu_count()
    return 1 if n == 1 else n // 2

bind = '0.0.0.0:5000'
workers = get_worker_size()
errorlog = 'log/error.log'
accesslog = 'log/access.log'
