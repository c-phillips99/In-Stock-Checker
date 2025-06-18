# checker/notifier.py
import time
import random
import requests
from checker import utils
from checker.run_schedule import run_schedule

def send_discord_alert(message, webhook_url, user_id, retries=2):
    payload = {"content": f"<@{user_id}> {message}"}
    for attempt in range(retries + 1):
        try:
            res = requests.post(webhook_url, json=payload, timeout=10)
            if res.status_code == 204:
                run_schedule.set_last_alert_time()
                return
            
        except Exception as e:
            if attempt == retries:
                utils.log_error(f"Discord alert failed: {e}")
            else:
                time.sleep(random.uniform(2, 4))

def build_discord_message(url, price, domain):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return (
        "🚨 **IN STOCK ALERT**\n"
        f"**Store:** {domain}\n"
        f"**Price:** {price}\n"
        f"🔗 [View Product]({url})\n\n"
        f"🕒 Checked at: {timestamp}"
    )