"""
    Carga datos desde un archivo JSON.
    Si el archivo no existe o está vacío,
    retorna una lista vacía.

    """

import json
import os


def load_data(file_path: str) -> list:

    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        # Si el JSON está vacío o corrupto
        return []


def save_data(file_path: str, data: list) -> None:
    """
    Guarda datos dentro de un archivo JSON.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )