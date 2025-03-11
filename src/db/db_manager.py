import os
from datetime import timezone
from dotenv import load_dotenv
from db.models import NotionDB
from db.database import engine, Base
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.Session = sessionmaker(bind=engine)
        self.db_url = os.getenv("DATABASE_URL")
        self.init_database()

    def init_database(self):
        if not database_exists(self.db_url):
            print("creating database...")
            create_database(self.db_url)
        else:
            print("database already exist.")
        Base.metadata.create_all(bind=engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise
        finally:
            session.close()

    def add_notion_db_paper_info(self, paper_info):
        with self.session_scope() as session:
            new_paper = NotionDB(**paper_info)
            session.add(new_paper)
            print("Registered successfully")

    def check_paper_exists(self, paper_id=None, file_name=None):
        with self.session_scope() as session:
            if paper_id:
                exists = session.query(NotionDB).filter_by(id=paper_id).first() is not None
            elif file_name:
                exists = session.query(NotionDB).filter_by(file_name=file_name).first() is not None
            return exists

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.init_database()
    print("Database initialized.")
    is_exist = db_manager.check_paper_exists("1ac4e814-e366-81a7-875b-f0f2d7c13374")
    print(f"already exist?: {is_exist}")