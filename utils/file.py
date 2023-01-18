import shutil
import os

from werkzeug.datastructures import FileStorage


class TmpFileStorage:

    tmp_root: str
    file: FileStorage
    file_root: str

    @staticmethod
    def init_tmpfile(tmp_root: str):
        TmpFileStorage.tmp_root = tmp_root
        if os.path.isdir(tmp_root):
            shutil.rmtree(tmp_root)
        os.mkdir(tmp_root)

    def __init__(self, file: FileStorage):
        self.file = file
        self.file_root = f'{self.tmp_root}/{file.filename}'

    def __str__(self):
        return self.file_root

    def save(self):
        if not os.path.isfile(self.file_root):
            self.file.save(self.file_root)

    def remove(self):
        if os.path.isfile(self.file_root):
            os.remove(self.file_root)