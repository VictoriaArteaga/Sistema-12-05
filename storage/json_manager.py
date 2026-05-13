# JSON Storage Manager
# Provides functions to load and save data to JSON files.

import json
import os
from typing import List


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
