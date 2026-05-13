# Validators
# Reusable validation functions for business logic.

import re
from typing import List, Optional


def validate_email(email: str) -> bool:
    """
    Validates that an email address has a valid format.

    Args:
        email: Email address to validate.

    Returns:
        True if the format is valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_not_empty(value: str, field_name: str = "field") -> str:
    """
    Validates that a text field is not empty.

    Args:
        value: Value to validate.
        field_name: Name of the field (for error messages).

    Returns:
        The value stripped of leading/trailing whitespace.

    Raises:
        ValueError: If the value is empty or only whitespace.
    """
    if not value or not isinstance(value, str) or not value.strip():
        raise ValueError(f"The {field_name} cannot be empty.")
    return value.strip()


def validate_salary(salary: Optional[float]) -> Optional[float]:
    """
    Validates that the salary is a positive number (if provided).

    Args:
        salary: Salary to validate (can be None).

    Returns:
        The validated salary or None.

    Raises:
        ValueError: If the salary is negative or zero.
    """
    if salary is None:
        return None

    try:
        salary = float(salary)
    except (TypeError, ValueError):
        raise ValueError("The salary must be a numeric value.")

    if salary <= 0:
        raise ValueError("The salary must be greater than zero.")

    return salary


def validate_skills(skills: List[str]) -> List[str]:
    """
    Validates and cleans a list of skills.

    Args:
        skills: List of skills to validate.

    Returns:
        List of skills without duplicates and extra whitespace removed.

    Raises:
        ValueError: If the list is empty or contains no valid skills.
    """
    if not skills or not isinstance(skills, list):
        raise ValueError("You must provide at least one skill.")

    # Clean and filter empty skills
    cleaned = []
    seen = set()
    for skill in skills:
        if isinstance(skill, str) and skill.strip():
            skill_clean = skill.strip()
            skill_lower = skill_clean.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                cleaned.append(skill_clean)

    if not cleaned:
        raise ValueError("You must provide at least one valid skill.")

    return cleaned


def validate_status(status: str, valid_statuses: List[str]) -> str:
    """
    Validates that a status is one of the allowed values.

    Args:
        status: Status to validate.
        valid_statuses: List of valid statuses.

    Returns:
        The validated status in lowercase.

    Raises:
        ValueError: If the status is not valid.
    """
    if not status or not isinstance(status, str):
        raise ValueError("The status cannot be empty.")

    status_lower = status.strip().lower()

    if status_lower not in [s.lower() for s in valid_statuses]:
        valid_str = ", ".join(valid_statuses)
        raise ValueError(f"Invalid status: '{status}'. Allowed values: {valid_str}")

    return status_lower
