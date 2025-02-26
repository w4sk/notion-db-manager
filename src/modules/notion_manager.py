import subprocess


class NotionManager:
    def __init__(self):
        pass

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
            process = subprocess.run(f"papnt paths {path}", capture_output=True, text=True, check=True, shell=True)
            print(process.stdout)
            print(f"Succesfully registered paper info by path")
        except Exception as e:
            print(f"Error: {e}")
