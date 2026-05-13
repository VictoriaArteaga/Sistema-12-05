# storage/json_manager.py
import json
import os

class JSONManager:
    def __init__(self, base_path="storage/data"):
        self.base_path = base_path
        if not os.path.exists(self.base_path): os.makedirs(self.base_path)

    def load_data(self, filename: str) -> list:
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path): return []
        try:
            with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
        except: return []

    def save_data(self, filename: str, data: list) -> None:
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)
