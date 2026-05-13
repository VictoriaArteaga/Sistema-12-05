# Helper Functions
# General utilities for formatting, searching, and data presentation.

from datetime import datetime
from typing import List, Optional


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


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncates a long text by appending '...' at the end.

    Args:
        text: Text to truncate.
        max_length: Maximum allowed length.

    Returns:
        Truncated text if it exceeds the limit.
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


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
