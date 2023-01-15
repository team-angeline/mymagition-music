import shutil
import os

TMP_ROOT = 'tmp'

def init_tmp_dir():
    if os.path.isdir(TMP_ROOT):
        shutil.rmtree(TMP_ROOT)
    os.mkdir(TMP_ROOT)