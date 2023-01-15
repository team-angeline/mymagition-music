import random
import string

from loader.tmp import TMP_ROOT


def generate_randomize_id() -> str:
    return ''.join(
        random.choice(
            string.ascii_lowercase + string.digits
        ) for _ in range(50))

def generate_file_root(client_id: str, topic: str):
    return f'{TMP_ROOT}/{topic}-{client_id}'
