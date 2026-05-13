# Recruiter (Employer) Management Service
# Contains all business logic for recruiter/company management.

import os
from typing import List, Optional

from models.recruiter import Recruiter
from storage.json_manager import load_data, save_data
from utils.validators import validate_email, validate_not_empty


class RecruiterService:
    """
    Service to manage recruiters (employers) on the platform.

    Responsibilities:
    - Register new companies/recruiters with validations.
    - Query recruiters (all, by ID, by email).
    - Update company data.
    - Search by company name or industry.
    - Delete recruiters.
    """

    FILE_PATH = os.path.join("storage", "data", "recruiters.json")

    # ────────────────────────────────────────────
    #  Internal persistence methods
    # ────────────────────────────────────────────

    @classmethod
    def _get_all_recruiters_data(cls) -> List[dict]:
        """Gets all recruiter data as dictionaries."""
        try:
            return load_data(cls.FILE_PATH)
        except Exception:
            return []

    @classmethod
    def _save_all_recruiters_data(cls, data: List[dict]) -> None:
        """Saves all recruiter data."""
        save_data(cls.FILE_PATH, data)

    # ────────────────────────────────────────────
    #  Registration
    # ────────────────────────────────────────────

    @classmethod
    def register_recruiter(cls, company_name: str, email: str, industry: str) -> Recruiter:
        """
        Registers a new recruiter/company in the system.

        Business rules:
        - Company name cannot be empty.
        - Email must have a valid format.
        - Two recruiters cannot register with the same email.
        - Industry/sector cannot be empty.
        """
        # Validations
        company_name = validate_not_empty(company_name, "company name")
        industry = validate_not_empty(industry, "industry/sector")
        email_clean = email.strip().lower() if email else ""

        if not validate_email(email_clean):
            raise ValueError("The email address does not have a valid format.")

        # Business rule: unique email among recruiters
        if cls.get_recruiter_by_email(email_clean):
            raise ValueError(f"A recruiter with the email '{email_clean}' already exists.")

        # Create and persist
        new_recruiter = Recruiter(
            company_name=company_name,
            email=email_clean,
            industry=industry
        )

        recruiters_data = cls._get_all_recruiters_data()
        recruiters_data.append(new_recruiter.to_dict())
        cls._save_all_recruiters_data(recruiters_data)

        return new_recruiter

    # ────────────────────────────────────────────
    #  Queries
    # ────────────────────────────────────────────

    @classmethod
    def get_all_recruiters(cls) -> List[Recruiter]:
        """Returns the complete list of registered recruiters."""
        recruiters_data = cls._get_all_recruiters_data()
        return [Recruiter.from_dict(data) for data in recruiters_data]

    @classmethod
    def get_recruiter_by_id(cls, recruiter_id: str) -> Optional[Recruiter]:
        """Finds a recruiter by their ID."""
        recruiters = cls.get_all_recruiters()
        for recruiter in recruiters:
            if recruiter.id == recruiter_id:
                return recruiter
        return None

    @classmethod
    def get_recruiter_by_email(cls, email: str) -> Optional[Recruiter]:
        """Finds a recruiter by their email address."""
        if not email:
            return None

        email_lower = email.strip().lower()
        recruiters = cls.get_all_recruiters()
        for recruiter in recruiters:
            if recruiter.email.lower() == email_lower:
                return recruiter
        return None

    # ────────────────────────────────────────────
    #  Update
    # ────────────────────────────────────────────

    @classmethod
    def update_recruiter(cls, recruiter_id: str, company_name: Optional[str] = None,
                         email: Optional[str] = None, industry: Optional[str] = None) -> Optional[Recruiter]:
        """Updates the data of an existing recruiter. Only provided (non-None) fields are updated."""
        recruiters = cls.get_all_recruiters()
        recruiter_updated = False

        for recruiter in recruiters:
            if recruiter.id == recruiter_id:
                if company_name is not None:
                    recruiter.company_name = validate_not_empty(company_name, "company name")
                if email is not None:
                    email_clean = email.strip().lower()
                    if not validate_email(email_clean):
                        raise ValueError("The email address does not have a valid format.")
                    existing = cls.get_recruiter_by_email(email_clean)
                    if existing and existing.id != recruiter_id:
                        raise ValueError(f"The email '{email_clean}' is already in use by another recruiter.")
                    recruiter.email = email_clean
                if industry is not None:
                    recruiter.industry = validate_not_empty(industry, "industry/sector")
                recruiter_updated = True
                break

        if recruiter_updated:
            recruiters_data = [r.to_dict() for r in recruiters]
            cls._save_all_recruiters_data(recruiters_data)
            return cls.get_recruiter_by_id(recruiter_id)
        return None

    # ────────────────────────────────────────────
    #  Search
    # ────────────────────────────────────────────

    @classmethod
    def search_by_company(cls, company_name: str) -> List[Recruiter]:
        """Searches for recruiters whose company name contains the given text."""
        if not company_name or not company_name.strip():
            return []
        name_lower = company_name.strip().lower()
        recruiters = cls.get_all_recruiters()
        return [r for r in recruiters if name_lower in r.company_name.lower()]

    @classmethod
    def search_by_industry(cls, industry: str) -> List[Recruiter]:
        """Searches for recruiters by sector/industry."""
        if not industry or not industry.strip():
            return []
        industry_lower = industry.strip().lower()
        recruiters = cls.get_all_recruiters()
        return [r for r in recruiters if industry_lower in r.industry.lower()]

    # ────────────────────────────────────────────
    #  Deletion
    # ────────────────────────────────────────────

    @classmethod
    def delete_recruiter(cls, recruiter_id: str) -> bool:
        """Deletes a recruiter from the system by their ID."""
        recruiters_data = cls._get_all_recruiters_data()
        original_count = len(recruiters_data)
        recruiters_data = [r for r in recruiters_data if r.get("id") != recruiter_id]
        if len(recruiters_data) < original_count:
            cls._save_all_recruiters_data(recruiters_data)
            return True
        return False
