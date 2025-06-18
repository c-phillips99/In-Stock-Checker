# checker/error_handler.py
from checker import utils

def handle_unexpected_exception(e, url):
    if "Timed out receiving message from renderer" in str(e):
        utils.log_error(f"Renderer timeout on {url}")
        return f"⚠️ Renderer timeout: {url}"
    utils.log_error(f"Exception for {url}: {e}")
    return f"⚠️ Error with {url}: {e}"