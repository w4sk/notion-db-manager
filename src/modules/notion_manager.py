import requests
from dotenv import load_dotenv
import os
import subprocess

class NotionManager:
    def __init__(self):
        load_dotenv()
        self.notion_database_url = os.getenv("NOTION_DATABASE_URL")
        self.notion_token_id = os.getenv("NOTION_TOKEN_ID")
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")

    def register_paper_info_by_doi(self):
        try:
            print("Registering paper info by DOI...")
            process = subprocess.run("papnt doi", capture_output=True, text=True, check=True, shell=True)
            print(process.stdout)
            print(f"Succesfully registered paper info by DOI")
        except Exception as e:
            print(f"Error: {e}")

    def register_paper_info_by_pdf(self):
        try:
            print("Registering paper info by PDF...")
            process = subprocess.run("papnt pdf", capture_output=True, text=True, check=True, shell=True)
            print(process.stdout)
            print(f"Succesfully registered paper info by PDF")
        except Exception as e:
            print(f"Error: {e}")

    def register_paper_info_by_path(self, path):
        try:
            print("Registering paper info by path...")
            process = subprocess.run(["papnt", "paths", path], capture_output=True, text=True, check=True)
            print(process.stdout)
            print(f"Succesfully registered paper info by path")
        except subprocess.CalledProcessError as e:
            print(f"Error: papnt command failed with return code {e.returncode}. Output: {e.stderr}")
        except FileNotFoundError:
            print(f"Error: papnt command not found. Is it installed and in your PATH?")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def get_registered_paper_info(self):
        try:
            url = f"https://api.notion.com/v1/databases/{self.notion_database_id}/query"
            headers = {
                "Authorization": f"Bearer {self.notion_token_id}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
            
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            results = response.json()["results"]
            paper_info_list = []
            for result in results:
                paper_info = {
                    "id": result['id'],
                    "created_time": result['created_time'],
                    "last_edited_time": result['last_edited_time'],
                    "title": result['properties']['Title']['rich_text'][0]['plain_text'] if result['properties']['Title']['rich_text'] else None,
                    "doi": result['properties']['DOI']['rich_text'][0]['plain_text'] if result['properties']['DOI']['rich_text'] else None,
                }
                paper_info_list.append(paper_info)
            return paper_info_list
        except Exception as e:
            print(f"Error occurred when getting registered paper DOI: {e}")