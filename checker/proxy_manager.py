# checker/proxy.py
import json, random
import requests
import concurrent.futures
from pathlib import Path
from fp.fp import FreeProxy  # type: ignore
from checker import utils


class ProxyManager:
    def __init__(self):
        self.whitelist_file = Path("data/proxy_whitelist.json")
        self.blacklist_file = Path("data/proxy_blacklist.json")
        self.whitelist = set()
        self.blacklist = set()
        self.proxy_test_urls = [
            "https://www.walmart.com/",
            "https://www.target.com/",
            "https://www.gamestop.com/",
            "https://www.newegg.com/",
            "https://www.amazon.com/"
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80"
        ]
        self.load()

    def load(self):
        if self.whitelist_file.exists():
            self.whitelist = set(json.loads(self.whitelist_file.read_text()))
        if self.blacklist_file.exists():
            self.blacklist = set(json.loads(self.blacklist_file.read_text()))

    def save(self):
        utils.safe_write(self.whitelist_file, list(self.whitelist))
        utils.safe_write(self.blacklist_file, list(self.blacklist))

    def test_proxy(self, proxy, max_attempts=3):
        test_urls = random.sample(self.proxy_test_urls, k=min(max_attempts, len(self.proxy_test_urls)))
        for test_url in test_urls:
            try:
                response = requests.get(
                    test_url,
                    proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                    headers={"User-Agent": random.choice(self.user_agents)},
                    timeout=7
                )
                if response.status_code in [200, 301, 302]:
                    return True
            except:
                pass
        return False

    def try_fetch_proxy(self):
        try:
            return FreeProxy(timeout=3, rand=True, anonym=True, https=True).get()
        except:
            return None

    def fetch_proxy_with_timeout(self, timeout=5):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.try_fetch_proxy)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                return None

    def get_random_https_proxy(self, max_retries=10):
        whitelist = list(self.whitelist)
        random.shuffle(whitelist)
        for proxy in whitelist:
            if self.test_proxy(proxy):
                return proxy
            else:
                self.blacklist.add(proxy)
                self.whitelist.discard(proxy)
                self.save()

        for _ in range(max_retries):
            proxy = self.fetch_proxy_with_timeout()
            if not proxy or proxy in self.blacklist:
                continue
            if self.test_proxy(proxy):
                self.whitelist.add(proxy)
                self.save()
                return proxy
            else:
                self.blacklist.add(proxy)
        self.save()
        return None
    
proxy_manager = ProxyManager()