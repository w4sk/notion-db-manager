import datetime
from db.database import Base
from sqlalchemy import Column, String, DateTime


class NotionDB(Base):
    __tablename__ = "notion_db"

    id = Column(String, primary_key=True)
    created_time = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    last_edited_time = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    title = Column(String)
    doi = Column(String, nullable=False)

    def __repr__(self):
        return f"<NotionDB(id={self.id}, created_time={self.created_time}, last_edited_time={self.last_edited_time}, title={self.title}, doi={self.doi})>"
