import os
import time
from datetime import timedelta

import fitz  # PyMuPDF
import re


class PaperAnalyzer:
    def __init__(self):
        self.paper_dir = os.getenv("PAPER_DIR")

    def get_paper_name(self, duration=timedelta(days=1)):
        new_file = []
        if not os.path.exists(self.paper_dir):
            raise FileNotFoundError(f"Directory not found: {self.paper_dir}")
        
        threshold_time = time.time() - duration.total_seconds()
        with os.scandir(self.paper_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    try:
                        file_time = entry.stat().st_birthtime
                    except AttributeError:
                        file_time = entry.stat().st_mtime
                    if file_time >= threshold_time:
                        new_file.append(entry.name)
        return new_file
    def get_keywords(self, path):
        pdf_path = path
        HEADER_PATTERN = re.compile(r'(?:\bkey\s*[-\s]*word(?:s)?\b|\bkey\b|Index Terms)', re.IGNORECASE)
        origin = fitz.open(pdf_path)

        if len(origin) > 0:
            page_text = origin[0].get_text("text")
            lines = page_text.splitlines()
            crop_start = len(lines) // 9
            crop_end = len(lines) - (len(lines) // 5)

            page = "\n".join(lines[crop_start:crop_end])

        lines = page.splitlines()
        section_text = ""
        found_kw_flg = False

        for line in lines:
            stripped_line = line.strip()
            if not found_kw_flg:
                if bool(HEADER_PATTERN.search(line)):
                    found_kw_flg = True
                    # print(line)
                m = HEADER_PATTERN.search(line)
                if m:
                    line = line[m.end():].lstrip("—: ").strip()
                    section_text += " " + line
            else:
                if stripped_line == "":
                    break
                section_text += " " + stripped_line

        """
        洗浄してトークン化
        """
        # 改行時のハイフンやイコール記号の除去
        section_text = re.sub(r'-\s+', '', section_text)
        section_text = re.sub(r'=\s*', '', section_text)


        s = section_text.replace('\n', ' ').strip()
        words = re.split(r'[\s_-]+', s)
        words = [word for word in words if word]
        section_text =  ''.join(word.capitalize() for word in words)

        print(section_text)

        tokens = re.split(r"[;,]", section_text)

        print(tokens)


        end_flg = False
        keywords = []
        for token in tokens:
            token = token.strip()

            if not token:
                continue

            if 'I.I' in token:
                token = token.split('I.I')[0].strip()
                # keywords.append(token)
                end_flg = True
            if '.' in token:
                token = token.split('.')[0].strip()
                # keywords.append(token)
                end_flg = True

            if 'Acm' in token:
                token = token.split('Acm')[0].strip()
                # keywords.append(token)
                end_flg = True
            if '1' in token:
                token = token.split('1')[0].strip()
                # keywords.append(token)
                end_flg = True

            # 大文字がn文字以上ならスルー
            count_upper = sum(1 for c in token if c.isupper())
            if count_upper >= 7:
                break

            
            keywords.append(token)
            # キーワードがｎ個以上 or endフラグ立ってたら終了
            if len(keywords) >= 15 or end_flg:
                break
        if len(keywords) == 0:
            keywords.append("None")

        print(keywords)
