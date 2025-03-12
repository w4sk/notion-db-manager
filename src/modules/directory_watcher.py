import os
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEvent, FileSystemEventHandler
from modules.paper_analyzer import PaperAnalyzer


class DirectoryWatcher:
    def __init__(self, handler=FileSystemEventHandler()):
        load_dotenv()
        self.observer = Observer()
        self.handler = handler
        self.directory = os.getenv("PAPER_DIR")

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join()
        except KeyboardInterrupt:
            self.observer.stop()
