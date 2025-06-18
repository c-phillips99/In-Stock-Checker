# checker/stock_handler.py
from checker.cache_manager import cache_manager
from checker.stock_checkers import site_check_logic, get_price_from_page
from checker.notifier import send_discord_alert, build_discord_message

def process_stock_status_and_alert(url, page, config, domain):
    if site_check_logic(url, page):
        price = get_price_from_page(url, page)
        cache_manager.update_stock_data(url, price, domain)
        message = build_discord_message(url, price, domain)
        send_discord_alert(message, config["discord_webhook_url"], config["discord_user_id"])
        return f"   ✅ ALERT SENT — Price: {price}"
    else:
        return f"   ❌ Out of stock"