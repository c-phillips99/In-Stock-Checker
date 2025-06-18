# checker/browser.py
import random
import undetected_chromedriver as uc
from checker.proxy_manager import proxy_manager
from checker.constants import CAPTCHA_FORM, VERIFY_HUMAN, ACCESS_DENIED

def get_driver(use_proxies=True):
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=AutomationControlled")
    options.add_argument(f"--window-size={random.randint(1024, 1920)},{random.randint(768, 1080)}")
    options.add_argument(f"user-agent={random.choice(proxy_manager.user_agents)}")

    if use_proxies:
        proxy = proxy_manager.get_random_https_proxy()
        if proxy:
            options.add_argument(f"--proxy-server=http://{proxy}")

    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)

    try:
        driver.set_window_position(-2000, 0)
    except Exception as e:
        print(f"⚠️ Could not move window: {e}")

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
        });
        Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
        });
        """
    })
    return driver


def is_blocked_selenium(driver):
    try:
        if driver.find_elements("xpath", f"//form[contains(@action, '{CAPTCHA_FORM}')]"):
            return True
        if driver.find_elements("xpath", f"//*[contains(text(), '{VERIFY_HUMAN}')]"):
            return True
        if driver.find_elements("xpath", f"//*[contains(text(), '{ACCESS_DENIED}')]"):
            return True
        return False
    except:
        return False
    
def close_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing driver: {e}")
    finally:
        driver = None