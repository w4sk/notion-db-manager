import os
from dotenv import load_dotenv
from modules.paper_analyzer import PaperAnalyzer
from modules.notion_manager import NotionManager
from modules.slack_messenger import SlackMessenger


def main():
    load_dotenv()
    paper_analyzer = PaperAnalyzer()
    slack_messenger = SlackMessenger()
    notion_manager = NotionManager()

    new_files = paper_analyzer.get_paper_name()
    for new_file in new_files:
        new_file_path = os.path.join(paper_analyzer.paper_dir, new_file)
        new_file_path = os.path.abspath(new_file_path)
        notion_manager.register_paper_info_by_path(new_file_path)
        slack_messenger.send_message(f"New paper: <{notion_manager.notion_database_url}|{new_file}>")


if __name__ == "__main__":
    main()
