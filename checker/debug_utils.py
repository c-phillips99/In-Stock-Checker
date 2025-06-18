# checker/debug_utils.py

from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

def get_domain(url):
    host = urlparse(url).netloc
    return host.replace('.', '_')

def save_debug_snapshot(domain, content, suffix="html"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(f"debug/{domain}_{timestamp}.{suffix}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def save_error_log(url, exception):
    domain = get_domain(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    message = f"[{timestamp}] Exception for {url}: {exception}"
    path = Path(f"debug/{domain}_{timestamp}_error.txt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message)
    return message
