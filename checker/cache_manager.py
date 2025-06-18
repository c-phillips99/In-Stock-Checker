# checker/cache_manager.py
import json, time
from pathlib import Path
from checker import utils

class CacheManager:
    def __init__(self):
        self.file = Path("data/in_stock_cache.json")
        self.in_stock_cache = {}
        self.load()

    def load(self):
        if self.file.exists():
            try:
                self.in_stock_cache = json.loads(self.file.read_text())
                print (f"[CACHE LOAD] Loaded cache with {len(self.in_stock_cache)} items")
            except Exception as e:
                utils.log_error(f"[CACHE LOAD ERROR] Failed to read cache: {e}")
                return

    def save(self):
        print(f"[CACHE SAVE] Saving {len(self.in_stock_cache)} items")
        utils.safe_write(self.file, self.in_stock_cache)

    def clear(self):
        print("[CACHE CLEAR] Clearing cache")
        self.in_stock_cache = {}
        self.save()

    def get_cache(self):
        if not self.in_stock_cache:
            print("[CACHE GET] Cache is empty!")
        return self.in_stock_cache
    
    def set_expired(self, url):
        print(f"[CACHE EXPIRE] Setting {url} as expired")
        if url in self.in_stock_cache:
            self.in_stock_cache[url]["expired"] = True
            self.save()
        else:
            print(f"[CACHE EXPIRE] URL {url} not found in cache")

    def prune(self, alert_interval):
        if not self.in_stock_cache:
            print("[CACHE PRUNE] Skipping prune — cache is empty!")
            return

        now = time.time()
        to_delete = []

        for url, data in self.in_stock_cache.items():
            if not isinstance(data, dict):
                continue

            if now - data.get("timestamp", 0) > alert_interval:
                to_delete.append(url)

        for url in to_delete:
            print(f"[CACHE PRUNE] Deleting expired item: {url}")
            del self.in_stock_cache[url]

        if to_delete:
            self.save()
    
    def update_stock_data(self, url, price, domain):
        print(f"[DEBUG] update_stock_data: {url} | price={price} | domain={domain}")
        product_type = "Bundle" if "bundle" in url.lower() or "mario-kart" in url.lower() else "Console"
        self.in_stock_cache[url] = {
            "price": price,
            "domain": domain,
            "timestamp": time.time(),
            "expired": False,
            "type": product_type
        }
        self.save()
    
    def get_last_update_time(self):
        return max((data.get("timestamp", 0) for data in self.in_stock_cache.values()), default=0)

cache_manager = CacheManager()