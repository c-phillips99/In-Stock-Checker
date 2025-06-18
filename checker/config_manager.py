# checker/config_manager.py
import json
from pathlib import Path

class ConfigManager:
    _instance = None

    def __init__(self):
        if ConfigManager._instance is not None:
            raise Exception("Use ConfigManager.get() instead.")
        self.config_path = Path("data/config.json")
        self.config = self._load_config()

    @staticmethod
    def get():
        if ConfigManager._instance is None:
            ConfigManager._instance = ConfigManager()
        return ConfigManager._instance.config

    def _load_config(self):
        with self.config_path.open() as f:
            return json.load(f)
