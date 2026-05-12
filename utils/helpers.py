"""Funciones auxiliares para la bolsa de trabajo."""

import uuid
import re
from datetime import datetime
from typing import Any, List, Dict, TypeVar, Callable


T = TypeVar('T')


def generate_id() -> str:
    """Genera un identificador único."""
    return str(uuid.uuid4())


def get_current_date() -> str:
    """Obtiene la fecha actual en formato ISO."""
    return datetime.now().isoformat()


def get_formatted_date(date_string: str, date_format: str = "%d/%m/%Y") -> str:
    """Convierte fecha ISO a formato personalizado."""
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime(date_format)
    except ValueError as e:
        raise ValueError(f"Fecha inválida: {date_string}") from e


def is_valid_email(email: str) -> bool:
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_empty_or_whitespace(text: str) -> bool:
    """Verifica si un string está vacío o solo tiene espacios."""
    return not text or not text.strip()


def is_valid_string_length(
    text: str,
    min_chars: int = 1,
    max_chars: int = 255
) -> bool:
    """Valida límites de longitud de string."""
    if not isinstance(text, str):
        return False
    return min_chars <= len(text) <= max_chars


def normalize_text(text: str) -> str:
    """Normaliza string: elimina espacios y convierte a minúsculas."""
    return text.strip().lower()


def capitalize_text(text: str) -> str:
    """Capitaliza la primera letra de cada palabra."""
    return ' '.join(word.capitalize() for word in text.split())


def truncate_text(text: str, max_chars: int, suffix: str = "...") -> str:
    """Trunca string a longitud máxima con sufijo."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - len(suffix)] + suffix


def remove_extra_whitespace(text: str) -> str:
    """Elimina espacios en blanco múltiples."""
    return ' '.join(text.split())


def search_candidates(
    candidates: List[Dict[str, Any]],
    query: str,
    search_fields: List[str]
) -> List[Dict[str, Any]]:
    """Busca candidatos según término en campos específicos."""
    normalized_query = normalize_text(query)
    return [
        candidate for candidate in candidates
        if any(
            normalized_query in normalize_text(str(candidate.get(field, "")))
            for field in search_fields
        )
    ]


def search_jobs(
    jobs: List[Dict[str, Any]],
    query: str,
    search_fields: List[str]
) -> List[Dict[str, Any]]:
    """Busca empleos según término en campos específicos."""
    normalized_query = normalize_text(query)
    return [
        job for job in jobs
        if any(
            normalized_query in normalize_text(str(job.get(field, "")))
            for field in search_fields
        )
    ]


def filter_items(
    items: List[T],
    condition: Callable[[T], bool]
) -> List[T]:
    """Filtra lista usando función de condición."""
    return [item for item in items if condition(item)]


def group_by_field(
    records: List[Dict[str, Any]],
    field_name: str
) -> Dict[Any, List[Dict[str, Any]]]:
    """Agrupa registros por campo específico."""
    grouped: Dict[Any, List[Dict[str, Any]]] = {}
    for record in records:
        key = record.get(field_name)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(record)
    return grouped


def remove_duplicates(
    records: List[Dict[str, Any]],
    unique_field: str
) -> List[Dict[str, Any]]:
    """Elimina duplicados según campo clave."""
    seen = set()
    result = []
    for record in records:
        key = record.get(unique_field)
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result


def sort_records(
    records: List[Dict[str, Any]],
    sort_field: str,
    descending: bool = False
) -> List[Dict[str, Any]]:
    """Ordena registros por campo."""
    return sorted(records, key=lambda x: x.get(sort_field, ""), reverse=descending)


def paginate_results(
    records: List[T],
    page_number: int = 1,
    records_per_page: int = 10
) -> tuple[List[T], int]:
    """Pagina resultados. Retorna (registros, total_páginas)."""
    if page_number < 1:
        page_number = 1
    start_index = (page_number - 1) * records_per_page
    end_index = start_index + records_per_page
    total_pages = (len(records) + records_per_page - 1) // records_per_page
    return records[start_index:end_index], total_pages


def format_skills_for_display(skills: List[str], delimiter: str = ", ") -> str:
    """Formatea lista de habilidades para mostrar."""
    return delimiter.join(str(skill).strip() for skill in skills if skill)