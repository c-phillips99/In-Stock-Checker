# checker/captcha_handler.py
from checker.browser import is_blocked_selenium
from checker import utils
from checker.cooldown_manager import cooldown_manager

def handle_captcha_and_throttle_if_needed(driver, url, config):
    if is_blocked_selenium(driver):
        domain = cooldown_manager.get_domain(url)
        cooldown_duration = config["cooldowns"].get(domain, 3600)
        cooldown_manager.set_cooldown(domain, cooldown_duration)
        utils.log_error(f"CAPTCHA triggered — throttling {domain} for {cooldown_duration // 60} min")
        return f"⚠️ CAPTCHA detected on {url} — throttling {domain} for {cooldown_duration // 60} min"
    return None