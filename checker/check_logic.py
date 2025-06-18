# checker/check_logic.py
from checker.cache_manager import cache_manager
from checker.cooldown_manager import cooldown_manager

def should_skip_check(url, now, alert_interval):
    domain = cooldown_manager.get_domain(url)
    if cooldown_manager.is_throttled(url):
        remaining = round((cooldown_manager.cooldowns[domain] - now) / 60, 1)
        return True, f"⏸️ Skipped {url} — {domain} in cooldown for {remaining} more min", domain
    if url in cache_manager.get_cache():
        data = cache_manager.get_cache()[url]
        if isinstance(data, dict) and (now - data.get("timestamp", 0) < alert_interval and data.get("expired", False)):
            return True, f"⏳ Skipped (recent alert found): {url}", domain
    return False, "", domain