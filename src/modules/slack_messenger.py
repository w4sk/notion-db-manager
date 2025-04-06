import os
from dotenv import load_dotenv
from slack_sdk import WebClient


class SlackMessenger:
    def __init__(self):
        load_dotenv()
        self.client = WebClient(token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"))
        self.user_ids = os.getenv("SLACK_TARGET_USER_ID")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")

    def get_user_ids(self):
        return self.user_ids.split(",") if self.user_ids else []

    def get_user_ids_for_personal(self):
        return self.user_id_for_personal

    def open_conversation(self, user_ids):
        res = self.client.conversations_open(users=user_ids)
        return res["channel"]["id"]

    def upload_file_to_dm(self, file_path, title, initial_comment, user_ids):
        if not user_ids:
            user_ids = self.get_user_ids()
        dm_channel_id = self.open_conversation(user_ids)
        result = self.client.files_upload_v2(
            channel=dm_channel_id, file=file_path, title=title, initial_comment=initial_comment
        )
        return result

    def upload_file_to_channel(self, file_path, title, initial_comment, channel_id=None):
        if not channel_id:
            channel_id = self.channel_id
        result = self.client.files_upload_v2(
            channel=channel_id, file=file_path, title=title, initial_comment=initial_comment
        )
        return result

    def send_message_to_dm(self, message, user_ids=None):
        user_ids = user_ids if user_ids else self.get_user_ids()
        dm_channel_id = self.open_conversation(user_ids)
        self.client.chat_postMessage(channel=dm_channel_id, text=message)

    def send_message_to_channel(self, message, channel_id=None):
        if not channel_id:
            channel_id = self.channel_id
        self.client.chat_postMessage(channel=channel_id, text=message)

    def get_bookmark_list(self):
        channel_id = self.channel_id_for_personal
        result = self.client.bookmarks_list(channel_id=channel_id)
        return result

    def add_bookmark(self, title, id, type="link"):
        channel_id = self.channel_id_for_personal
        link = f"https://drive.google.com/drive/u/0/folders/{id}"
        result = self.client.bookmarks_add(channel_id=channel_id, title=title, type=type, link=link)
        return result

    def remove_bookmark(self, bookmark_id):
        channel_id = self.channel_id_for_personal
        result = self.client.bookmarks_remove(channel_id=channel_id, bookmark_id=bookmark_id)
        return result
