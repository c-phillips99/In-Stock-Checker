# checker/cooldown_manager.py
import json, time
from pathlib import Path
from urllib.parse import urlparse
from checker import utils

class CooldownManager:
    _file = Path("data/domain_cooldown.json")

    def __init__(self):
        self.cooldowns = {}
        self.load()

    def load(self):
        if self._file.exists():
            self.cooldowns = json.loads(self._file.read_text())

    def save(self):
        utils.safe_write(self._file, self.cooldowns)

    def get_domain(self, url):
        host = urlparse(url).netloc.split('.')
        return host[-3] if host[-2] in ['com', 'co', 'org'] else host[-2]

    def is_throttled(self, url):
        dom = self.get_domain(url)
        return dom in self.cooldowns and time.time() < self.cooldowns[dom]

    def set_cooldown(self, domain, duration):
        self.cooldowns[domain] = time.time() + duration
        self.save()

cooldown_manager = CooldownManager()