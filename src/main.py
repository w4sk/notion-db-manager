import os
from dotenv import load_dotenv
from modules.paper_analyzer import PaperAnalyzer
from modules.notion_manager import NotionManager
from modules.slack_messenger import SlackMessenger
from db.db_manager import DatabaseManager

def sync_notion_db(notion_manager, db_manager):
    print("Syncing Notion database...")
    notion_registered_paper_info_list = notion_manager.get_registered_paper_info()
    for notion_registered_paper_info in notion_registered_paper_info_list:
        is_exist = db_manager.check_paper_exists(paper_id=notion_registered_paper_info["id"])
        if not is_exist:
            db_manager.add_notion_db_paper_info(notion_registered_paper_info)
    
def main():
    load_dotenv()
    paper_analyzer = PaperAnalyzer()
    slack_messenger = SlackMessenger()
    notion_manager = NotionManager()
    db_manager = DatabaseManager()
    db_manager.init_database()
    
    sync_notion_db(notion_manager, db_manager)

    new_files = paper_analyzer.get_paper_name()
    if new_files:
        print(f"New papers: {new_files}")
    for new_file in new_files:
        if new_file.endswith(".pdf") and not db_manager.check_paper_exists(file_name=new_file):
            new_file_path = os.path.join(paper_analyzer.paper_dir, new_file)
            new_file_path = os.path.abspath(new_file_path)
            notion_manager.register_paper_info_by_path(new_file_path)
            slack_messenger.send_message(f"New paper: <{notion_manager.notion_database_url}|{new_file}>")


if __name__ == "__main__":
    main()
