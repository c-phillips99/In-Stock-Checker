from checker.constants import ADD_TO_CART, OUT_OF_STOCK, PICK_IT_UP, BTN_DISABLED, SOLD_OUT, WALMART, TARGET, BESTBUY, SAMSCLUB, NOT_AVAILABLE, GAMESTOP, UNKNOWN_PRICE
import re

def site_check_logic(url, page):
    page = page.lower()
    if WALMART in url or SAMSCLUB in url:
        return ADD_TO_CART in page and OUT_OF_STOCK not in page
    elif "target.com" in url:
        return (
            (ADD_TO_CART in page or PICK_IT_UP in page)
            and NOT_AVAILABLE not in page
            and OUT_OF_STOCK not in page
            and SOLD_OUT not in page
        )
    elif BESTBUY in url:
        return (ADD_TO_CART in page and BTN_DISABLED not in page and SOLD_OUT not in page)
    return False


def get_price_from_page(url, page):
    if WALMART in url:
        match = re.search(r'"price":"?(\d+\.\d+)"?', page)
        if match:
            return f"${match.group(1)}"

    elif TARGET in url or BESTBUY in url:
        match = re.search(r'"price":\s*"?(\d+\.\d+)"?', page)
        if match:
            return f"${match.group(1)}"

    elif GAMESTOP in url:
        match = re.search(r'<span[^>]*class="sr-only"[^>]*>\s*\$(\d+\.\d+)', page)
        if match:
            return f"${match.group(1)}"

    # Fallback
    match = re.search(r'\$(\d{2,4}\.\d{2})', page)
    return match.group(0) if match else UNKNOWN_PRICE