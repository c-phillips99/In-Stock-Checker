# main.py

import time
import argparse
import asyncio

from checker.config_manager import ConfigManager
from checker.shared_state import check_lock
from checker import shared_state as state
from checker.cooldown_manager import cooldown_manager
from checker.cache_manager import cache_manager
from checker.run_schedule import run_schedule
from checker.runner import run_check_now

def wait_if_recently_checked():
    next_run = run_schedule.load()
    now = time.time()
    if next_run > now:
        wait_time = next_run - now
        mins, secs = divmod(int(wait_time), 60)
        readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_run))
        print(f"⏸️ Recently checked — delaying for {mins}m {secs}s (until {readable})\n")
        time.sleep(wait_time)

def print_active_cooldowns():
    now = time.time()
    active = {d: e for d, e in cooldown_manager.cooldowns.items() if e > now}
    if active:
        print("📦 Loaded cooldowns:")
        for domain, expiry in active.items():
            remaining = round((expiry - now) / 60, 1)
            print(f"  ⏳ {domain}: {remaining} minutes remaining")

def clear_stale_check_flag():
    if state.is_checking(stale_after=600) is False and state._check_file.exists():
        print("🧹 Removing stale check flag from previous crash...")
        state.set_checking(False)

async def main_loop():
    config = ConfigManager.get()
    check_interval = config.get("check_interval", 900)

    while True:
        run_schedule.next_run = run_schedule.load()
        should_wait, wait_time = run_schedule.should_wait()
        if should_wait:
            mins, secs = divmod(int(wait_time), 60)
            readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + wait_time))
            print(f"⏸️ Skipping check — rescheduled for {mins}m {secs}s (at {readable})\n")
            await asyncio.sleep(wait_time)
            continue

        if state.is_checking():
            print("⚠️ Another check is already running. Retrying in 5 seconds...\n")
            await asyncio.sleep(5)
            continue

        await run_check_now()
        await asyncio.sleep(check_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="In-Stock Checker")
    parser.add_argument("--use-proxies", action="store_true", help="Enable proxy usage for requests")
    args = parser.parse_args()

    config = ConfigManager.get()
    use_proxies = args.use_proxies or config.get("use_proxies", False)
    alert_interval = config.get("alert_interval", 3600)

    cache_manager.prune(alert_interval)
    wait_if_recently_checked()
    print_active_cooldowns()
    clear_stale_check_flag()

    asyncio.run(main_loop())
