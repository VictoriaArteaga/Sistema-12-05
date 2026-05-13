# storage/json_manager.py
import json
import os

class JSONManager:
    def __init__(self, base_path="storage/data"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _get_full_path(self, filename):
        return os.path.join(self.base_path, filename)

    def load_data(self, filename: str) -> list:
        file_path = self._get_full_path(filename)
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self, filename: str, data: list) -> None:
        file_path = self._get_full_path(filename)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def append_data(self, filename: str, item: dict) -> None:
        data = self.load_data(filename)
        data.append(item)
        self.save_data(filename, data)

    def find_by_field(self, filename: str, field: str, value: any) -> list:
        data = self.load_data(filename)
        return [item for item in data if item.get(field) == value]

    def find_by_id(self, filename: str, entity_id: str) -> dict:
        data = self.load_data(filename)
        for item in data:
            if item.get("id") == entity_id or item.get("uuid") == entity_id:
                return item
        return None

    def update_data(self, filename: str, entity_id: str, new_data: dict) -> bool:
        data = self.load_data(filename)
        for i, item in enumerate(data):
            if item.get("id") == entity_id or item.get("uuid") == entity_id:
                data[i] = new_data
                self.save_data(filename, data)
                return True
        return False

# Funciones de compatibilidad para código antiguo
_manager = JSONManager()

def load_data(file_path: str) -> list:
    # Si pasan una ruta completa, extraemos el nombre del archivo
    filename = os.path.basename(file_path)
    return _manager.load_data(filename)

def save_data(file_path: str, data: list) -> None:
    filename = os.path.basename(file_path)
    _manager.save_data(filename, data)