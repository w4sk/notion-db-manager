from modules.paper_analyzer import PaperAnalyzer
from modules.notion_manager import NotionManager
from modules.slack_messenger import SlackMessenger
from apscheduler.schedulers.background import BackgroundScheduler
from papnt.papnt.misc import load_config


class Admin:
    def __init__(self):
        self.paper_analyzer = PaperAnalyzer()
        self.notion_manager = NotionManager()
        self.slack_messenger = SlackMessenger()
        self.config = load_config("/usr/local/lib/python3.11/site-packages/papnt/config.ini")

    def check_duplicate_papers(self):
        def get_duplicate_paper_id():
            paper_ids = []
            duplicate_paper_ids = []
            registered_papers = self.notion_manager.get_registered_paper_info()
            for registered_paper in registered_papers:
                if registered_paper["doi"] in paper_ids:
                    duplicate_paper_ids.append(registered_paper["id"])
                paper_ids.append(registered_paper["doi"])
            return duplicate_paper_ids

        duplicate_paper_ids = get_duplicate_paper_id()
        if duplicate_paper_ids:
            self.notion_manager.delete_paper_records(duplicate_paper_ids)

    def register_paper_form_doi(self):
        no_info_registered_papers = self.notion_manager.get_registered_paper_info(use_is_checked=True)
        for no_info_registered_paper in no_info_registered_papers:
            self.notion_manager.register_paper_info_by_doi(
                no_info_registered_paper["doi"], self.config["misc"]["registered_by"]
            )


def admin_job(admin: Admin):
    admin.register_paper_form_doi()
    admin.check_duplicate_papers()


if __name__ == "__main__":
    admin = Admin()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(admin_job, 'cron', hour=2, minute=0)
    # scheduler.start()
    admin_job(admin)
