import os
import time
from datetime import timedelta


class PaperAnalyzer:
    def __init__(self):
        self.paper_dir = os.getenv("PAPER_DIR")

    def get_paper_name(self, duration=timedelta(days=1)):
        new_file = []
        if not os.path.exists(self.paper_dir):
            raise FileNotFoundError(f"Directory not found: {self.paper_dir}")
        
        threshold_time = time.time() - duration.total_seconds()
        with os.scandir(self.paper_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    file_time = entry.stat().st_mtime
                    if file_time > threshold_time:
                        new_file.append(entry.name)
        return new_file