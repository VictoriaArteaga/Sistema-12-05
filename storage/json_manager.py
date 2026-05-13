# JSON Storage Manager
# Provides functions and a class to load and save data to JSON files.

import json
import os
from typing import List, Optional


def load_data(file_path: str) -> List[dict]:
    """
    Loads a list of dictionaries from a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        List of dictionaries with the stored data.
        Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []


def save_data(file_path: str, data: List[dict]) -> None:
    """
    Saves a list of dictionaries to a JSON file.

    Creates the parent directory if it does not exist.

    Args:
        file_path: Path to the JSON file.
        data: List of dictionaries to save.
    """
    # Ensure the directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class JSONManager:
    """
    Class-based JSON storage manager.

    Provides higher-level methods like append, find_by_field,
    find_by_id, and update_data on top of the base load/save functions.
    """

    def __init__(self, base_path: str = "storage/data"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _get_full_path(self, filename: str) -> str:
        """Returns the full path for a given filename."""
        return os.path.join(self.base_path, filename)

    def load_data(self, filename: str) -> list:
        """Loads data from a JSON file by filename."""
        return load_data(self._get_full_path(filename))

    def save_data(self, filename: str, data: list) -> None:
        """Saves data to a JSON file by filename."""
        save_data(self._get_full_path(filename), data)

    def append_data(self, filename: str, item: dict) -> None:
        """Appends a single item to a JSON file."""
        data = self.load_data(filename)
        data.append(item)
        self.save_data(filename, data)

    def find_by_field(self, filename: str, field: str, value) -> list:
        """Finds all records matching a field value."""
        data = self.load_data(filename)
        return [item for item in data if item.get(field) == value]

    def find_by_id(self, filename: str, entity_id: str) -> Optional[dict]:
        """Finds a record by its 'id' or 'uuid' field."""
        data = self.load_data(filename)
        for item in data:
            if item.get("id") == entity_id or item.get("uuid") == entity_id:
                return item
        return None

    def update_data(self, filename: str, entity_id: str, new_data: dict) -> bool:
        """Updates a record by its ID, returns True if successful."""
        data = self.load_data(filename)
        for i, item in enumerate(data):
            if item.get("id") == entity_id or item.get("uuid") == entity_id:
                data[i] = new_data
                self.save_data(filename, data)
                return True
        return False
