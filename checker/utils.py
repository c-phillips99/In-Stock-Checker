# checker/utils.py
import json
import time
from pathlib import Path

def safe_write(path: Path, data):
    backup = path.with_suffix(".bak")
    if path.exists():
        path.rename(backup)
    try:
        path.write_text(json.dumps(data))
        if backup.exists():
            backup.unlink()
    except Exception as e:
        if backup.exists():
            backup.rename(path)
        raise e
    
def log_error(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    log_path = Path("data/error_log.txt")
    if log_path.exists() and log_path.stat().st_size > 5 * 1024 * 1024:
        log_path.rename(log_path.with_suffix(".bak"))
    with open(log_path, "a") as f:
        f.write(f"{timestamp} {message}\n")