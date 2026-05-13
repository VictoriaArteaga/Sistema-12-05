# Helper Functions
# General utilities for formatting, searching, and data presentation.

import uuid
import re
from datetime import datetime
from typing import Any, List, Dict, Optional, TypeVar, Callable


T = TypeVar('T')


# ────────────────────────────────────────────
#  Date & formatting utilities
# ────────────────────────────────────────────

def generate_id() -> str:
    """Generates a unique identifier."""
    return str(uuid.uuid4())


def get_current_date() -> str:
    """Returns the current date in ISO format."""
    return datetime.now().isoformat()


def format_date(iso_date: str) -> str:
    """
    Formats an ISO date into a human-readable format.

    Args:
        iso_date: Date in ISO 8601 format.

    Returns:
        Formatted date as 'DD/MM/YYYY HH:MM'.
    """
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return iso_date


def get_formatted_date(date_string: str, date_format: str = "%d/%m/%Y") -> str:
    """Converts an ISO date to a custom format."""
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime(date_format)
    except ValueError as e:
        raise ValueError(f"Invalid date: {date_string}") from e


def format_salary(salary: Optional[float]) -> str:
    """
    Formats a salary as currency.

    Args:
        salary: Salary value (can be None).

    Returns:
        Formatted salary or 'Not specified'.
    """
    if salary is None:
        return "Not specified"
    return f"${salary:,.2f}"


# ────────────────────────────────────────────
#  Text utilities
# ────────────────────────────────────────────

def is_valid_email(email: str) -> bool:
    """Validates email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_empty_or_whitespace(text: str) -> bool:
    """Checks if a string is empty or only whitespace."""
    return not text or not text.strip()


def is_valid_string_length(text: str, min_chars: int = 1, max_chars: int = 255) -> bool:
    """Validates string length limits."""
    if not isinstance(text, str):
        return False
    return min_chars <= len(text) <= max_chars


def normalize_text(text: str) -> str:
    """Normalizes a string: strips whitespace and converts to lowercase."""
    return text.strip().lower()


def capitalize_text(text: str) -> str:
    """Capitalizes the first letter of each word."""
    return ' '.join(word.capitalize() for word in text.split())


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncates a long text by appending a suffix at the end.

    Args:
        text: Text to truncate.
        max_length: Maximum allowed length.
        suffix: Suffix to append (default: '...').

    Returns:
        Truncated text if it exceeds the limit.
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def remove_extra_whitespace(text: str) -> str:
    """Removes multiple consecutive whitespace characters."""
    return ' '.join(text.split())


# ────────────────────────────────────────────
#  Search utilities
# ────────────────────────────────────────────

def search_in_text(query: str, *texts: str) -> bool:
    """
    Searches for a query (case-insensitive) in one or more texts.

    Args:
        query: Search term.
        *texts: Texts to search in.

    Returns:
        True if the query was found in at least one text.
    """
    if not query:
        return False

    query_lower = query.lower().strip()
    for text in texts:
        if text and query_lower in text.lower():
            return True
    return False


def search_candidates(candidates: List[Dict[str, Any]], query: str, search_fields: List[str]) -> List[Dict[str, Any]]:
    """Searches candidates by a term in specific fields."""
    normalized_query = normalize_text(query)
    return [
        candidate for candidate in candidates
        if any(
            normalized_query in normalize_text(str(candidate.get(field, "")))
            for field in search_fields
        )
    ]


def search_jobs(jobs: List[Dict[str, Any]], query: str, search_fields: List[str]) -> List[Dict[str, Any]]:
    """Searches jobs by a term in specific fields."""
    normalized_query = normalize_text(query)
    return [
        job for job in jobs
        if any(
            normalized_query in normalize_text(str(job.get(field, "")))
            for field in search_fields
        )
    ]


# ────────────────────────────────────────────
#  Collection utilities
# ────────────────────────────────────────────

def filter_items(items: List[T], condition: Callable[[T], bool]) -> List[T]:
    """Filters a list using a condition function."""
    return [item for item in items if condition(item)]


def group_by_field(records: List[Dict[str, Any]], field_name: str) -> Dict[Any, List[Dict[str, Any]]]:
    """Groups records by a specific field."""
    grouped: Dict[Any, List[Dict[str, Any]]] = {}
    for record in records:
        key = record.get(field_name)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(record)
    return grouped


def remove_duplicates(records: List[Dict[str, Any]], unique_field: str) -> List[Dict[str, Any]]:
    """Removes duplicates based on a key field."""
    seen = set()
    result = []
    for record in records:
        key = record.get(unique_field)
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result


def sort_records(records: List[Dict[str, Any]], sort_field: str, descending: bool = False) -> List[Dict[str, Any]]:
    """Sorts records by a field."""
    return sorted(records, key=lambda x: x.get(sort_field, ""), reverse=descending)


def paginate_results(records: List[T], page_number: int = 1, records_per_page: int = 10) -> tuple:
    """Paginates results. Returns (records, total_pages)."""
    if page_number < 1:
        page_number = 1
    start_index = (page_number - 1) * records_per_page
    end_index = start_index + records_per_page
    total_pages = (len(records) + records_per_page - 1) // records_per_page
    return records[start_index:end_index], total_pages


def format_skills_for_display(skills: List[str], delimiter: str = ", ") -> str:
    """Formats a skills list for display."""
    return delimiter.join(str(skill).strip() for skill in skills if skill)


# ────────────────────────────────────────────
#  Table display
# ────────────────────────────────────────────

def generate_summary_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Generates a formatted table for console display.

    Args:
        headers: List of column headers.
        rows: List of rows (each row is a list of values).

    Returns:
        String with the formatted table.
    """
    if not headers or not rows:
        return "No data to display."

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build separator line
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    # Build header line
    header_line = "|" + "|".join(
        f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)
    ) + "|"

    # Build rows
    row_lines = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            width = col_widths[i] if i < len(col_widths) else len(str(cell))
            cells.append(f" {str(cell):<{width}} ")
        row_lines.append("|" + "|".join(cells) + "|")

    # Assemble table
    lines = [separator, header_line, separator]
    for rl in row_lines:
        lines.append(rl)
    lines.append(separator)

    return "\n".join(lines)
