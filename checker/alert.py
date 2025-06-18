# checker/alert.py

import time
from checker import utils
from checker.browser import close_driver
from checker.captcha_handler import handle_captcha_and_throttle_if_needed
from checker.page_loader import load_driver_and_page
from checker.check_logic import should_skip_check
from checker.stock_handler import process_stock_status_and_alert
from checker.config_manager import ConfigManager
from checker.debug_utils import get_domain, save_debug_snapshot, save_error_log

def check_and_alert(url):
    config = ConfigManager.get()
    print(f"\n🔍 Checking:\n   {url}")
    now = time.time()

    should_skip, reason, domain = should_skip_check(url, now, config["alert_interval"])
    if should_skip:
        return reason

    driver, page_html, error = load_driver_and_page(url, config)
    if driver is None:
        return error

    try:
        captcha_result = handle_captcha_and_throttle_if_needed(driver, url, config)
        if captcha_result:
            return captcha_result

        if page_html:
            save_debug_snapshot(get_domain(url), page_html)

        return process_stock_status_and_alert(url, page_html, config, domain)

    except Exception as e:
        return save_error_log(url, e)

    finally:
        close_driver(driver)