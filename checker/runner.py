# checker/runner.py

import time
import random
import asyncio

from checker.alert import check_and_alert
from checker.cache_manager import cache_manager
from checker.shared_state import check_lock, set_checking
from checker.run_schedule import run_schedule
from checker.cooldown_manager import cooldown_manager
from checker.config_manager import ConfigManager

async def run_check_now():
    config = ConfigManager.get()
    urls_by_domain = config.get("urls", {})
    check_interval = config.get("check_interval", 900)
    alert_interval = config.get("alert_interval", 3600)

    if set_checking(True) is False:
        print("⚠️ Check already running.")
        return

    async with check_lock:
        try:
            print("🔁 Checking stock across domains...\n")
            domain_items = list(urls_by_domain.items())
            random.shuffle(domain_items)
            for domain, urls in domain_items:
                for url in urls:
                    result = await asyncio.to_thread(check_and_alert, url)
                    print(result)

            cache_manager.prune(alert_interval)

            jitter = random.uniform(-5 * 60, 5 * 60)
            next_run = time.time() + max(10 * 60, check_interval + jitter)
            run_schedule.save(next_run)

        finally:
            set_checking(False)