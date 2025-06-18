# checker/page_loader.py
import time
import random
from checker.browser import get_driver, close_driver

def load_page_with_retries(driver, url):
    for attempt in range(1, 3):
        try:
            print(f"   🌐 Attempt {attempt}: Visiting...")
            start = time.time()
            driver.get(url)
            duration = round(time.time() - start, 2)
            print(f"   ✅ Loaded in {duration}s")
            return driver.page_source, None
        except Exception as e:
            if "net::ERR_CONNECTION_TIMED_OUT" in str(e) and attempt < 2:
                print(f"   🔁 Timeout, retrying...")
                time.sleep(random.uniform(2, 4))
                continue
            return None, f"⚠️ Error loading page: {e}"

def load_driver_and_page(url, config):
    driver = get_driver(config.get("use_proxies", False))
    try:
        result = load_page_with_retries(driver, url)
        if result is None:
            return driver, None, "⚠️ Failed to load page and no error message returned"
        page_html, error = result
        time.sleep(random.uniform(8, 12))
        return driver, page_html, error
    except Exception as e:
        close_driver(driver)
        return None, None, f"⚠️ Error loading page: {e}"