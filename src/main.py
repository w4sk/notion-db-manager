import os
import threading
from dotenv import load_dotenv
from modules.paper_analyzer import PaperAnalyzer
from modules.notion_manager import NotionManager
from modules.slack_messenger import SlackMessenger
from modules.directory_watcher import DirectoryWatcher
from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEventHandler


class PaperHandler(FileSystemEventHandler):
    def __init__(self):
        self.paper_analyzer = PaperAnalyzer()
        self.notion_manager = NotionManager()
        self.slack_messenger = SlackMessenger()
        print("Starting to watch the directory...")

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        def register_to_notion():
            new_files = []
            if not event.is_directory and event.event_type == "created":
                new_files = [event.src_path.split("/")[-1]]
            else:
                return
            if new_files:
                print(f"New papers: {new_files}")
                for new_file in new_files:
                    if new_file.endswith(".pdf"):
                        new_file_path = os.path.join(self.paper_analyzer.paper_dir, new_file)
                        new_file_path = os.path.abspath(new_file_path)
                        keywords = self.paper_analyzer.get_keywords(new_file_path)
                        results = self.notion_manager.register_paper_info_by_path(new_file_path,keywords)
                        for key, value in results.items():
                            if value:
                                self.slack_messenger.send_message(
                                    f"New paper: <{self.notion_manager.notion_database_url}|{key}>"
                                )
                            else:
                                self.slack_messenger.send_message(
                                    f"Cannot register paper: {key}\nPlease register by yourself from <{self.notion_manager.notion_database_url}|here>"
                                )

        try:
            register_to_notion()

        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    load_dotenv()
    directory_watcher = DirectoryWatcher(handler=PaperHandler())
    directory_watcher.run()


if __name__ == "__main__":
    main()
