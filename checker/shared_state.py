# checker/shared_state.py
import asyncio
from pathlib import Path
import time

check_lock = asyncio.Lock()
_check_file = Path("data/is_checking.flag")

def set_checking(value: bool):
    if value:
        _check_file.write_text(str(int(time.time())))
    elif _check_file.exists():
        _check_file.unlink()


def is_checking(stale_after=600):  # 10 minutes default
    if not _check_file.exists():
        return False
    try:
        started_at = int(_check_file.read_text())
        return (time.time() - started_at) < stale_after
    except:
        _check_file.unlink()
        return False