import os
import json
import time
import unittest
from pathlib import Path
import sys

# Add project root to sys.path to allow imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from checker.cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.test_file = Path("data/test_in_stock_cache.json")
        self.cache = CacheManager()
        self.cache.file = self.test_file  # Override output path
        self.cache.clear

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
        backup = self.test_file.with_suffix(".bak")
        if backup.exists():
            backup.unlink()

    def test_update_stock_data_writes_to_file(self):
        url = "https://www.walmart.com/ip/Test-Item/123456"
        price = "$399.99"
        domain = "walmart"

        self.cache.update_stock_data(url, price, domain)

        # In-memory assertions
        self.assertIn(url, self.cache.get_cache())
        data = self.cache.get_cache()[url]
        self.assertEqual(data["price"], price)
        self.assertEqual(data["domain"], domain)
        self.assertIn("timestamp", data)
        self.assertEqual(data["type"], "Console")
        self.assertFalse(data["expired"])

        # On-disk assertions
        with open(self.test_file, "r") as f:
            on_disk = json.load(f)
            self.assertIn(url, on_disk)
            self.assertEqual(on_disk[url]["price"], price)

if __name__ == '__main__':
    unittest.main()
