import os

def file_ready(path: str) -> bool:
    return os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) > 0
