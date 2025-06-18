# checker/run_schedule.py
import time, json
from pathlib import Path
from checker import utils
from checker.constants import LAST_RUN_FILE, LAST_ALERT_FILE

class RunSchedule:
    def __init__(self, file_path=LAST_RUN_FILE):
        self.file = Path(file_path)
        self.next_run = self.load()

    def load(self):
        if self.file.exists():
            try:
                return json.loads(self.file.read_text()).get("next_run", 0)
            except Exception:
                return 0
        return 0

    def save(self, next_run_timestamp: float):
        now = time.time()
        self.next_run = next_run_timestamp
        data = {
            "next_run": int(next_run_timestamp),
            "last_run": int(now)
        }
        utils.safe_write(self.file, data)

    def should_wait(self):
        now = time.time()
        return self.next_run > now, self.next_run - now

    def readable_wait_time(self):
        wait = max(0, self.next_run - time.time())
        mins, secs = divmod(int(wait), 60)
        readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.next_run))
        return mins, secs, readable
    
    def get_last_run_time(self):
        if self.file.exists():
            try:
                return json.loads(self.file.read_text()).get("last_run", 0)
            except Exception:
                return 0
        return 0
    
    def set_last_alert_time(self):
        alert_file = Path(LAST_ALERT_FILE)
        utils.safe_write(alert_file, str(time.time()))

    def get_last_alert_time(self):
        alert_file = Path(LAST_ALERT_FILE)
        if alert_file.exists():
            try:
                return float(alert_file.read_text())
            except:
                return 0
        return 0
    
run_schedule = RunSchedule()