# User (Candidate) Management Service
# Contains all business logic for candidate management.

import os
from typing import List, Optional

from models.user import User
from storage.json_manager import load_data, save_data
from utils.validators import validate_email, validate_not_empty, validate_skills


class UserService:
    """
    Service to manage candidates on the platform.

    Responsibilities:
    - Register new candidates with validations.
    - Query candidates (all, by ID, by email).
    - Update professional profile.
    - Search candidates by skills.
    - Delete candidates.
    """

    FILE_PATH = os.path.join("storage", "data", "users.json")

    # ────────────────────────────────────────────
    #  Internal persistence methods
    # ────────────────────────────────────────────

    @classmethod
    def _get_all_users_data(cls) -> List[dict]:
        """Gets all user data as dictionaries."""
        try:
            return load_data(cls.FILE_PATH)
        except Exception:
            return []

    @classmethod
    def _save_all_users_data(cls, data: List[dict]) -> None:
        """Saves all user data."""
        save_data(cls.FILE_PATH, data)

    # ────────────────────────────────────────────
    #  Registration
    # ────────────────────────────────────────────

    @classmethod
    def register_user(cls, name: str, email: str, skills: List[str], resume: str) -> User:
        """
        Registers a new candidate in the system.

        Business rules:
        - Name cannot be empty.
        - Email must have a valid format.
        - Two candidates cannot register with the same email.
        - Must have at least one skill.
        """
        # Validations
        name = validate_not_empty(name, "name")
        email_clean = email.strip().lower() if email else ""

        if not validate_email(email_clean):
            raise ValueError("The email address does not have a valid format.")

        resume = validate_not_empty(resume, "professional summary")
        skills = validate_skills(skills)

        # Business rule: unique email
        if cls.get_user_by_email(email_clean):
            raise ValueError(f"A candidate with the email '{email_clean}' already exists.")

        # Create and persist
        new_user = User(name=name, email=email_clean, skills=skills, resume=resume)
        users_data = cls._get_all_users_data()
        users_data.append(new_user.to_dict())
        cls._save_all_users_data(users_data)
        return new_user

    # ────────────────────────────────────────────
    #  Queries
    # ────────────────────────────────────────────

    @classmethod
    def get_all_users(cls) -> List[User]:
        """Returns the complete list of registered candidates."""
        users_data = cls._get_all_users_data()
        return [User.from_dict(data) for data in users_data]

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[User]:
        """Finds a candidate by their ID."""
        users = cls.get_all_users()
        for user in users:
            if user.id == user_id:
                return user
        return None

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[User]:
        """Finds a candidate by their email address."""
        if not email:
            return None
        email_lower = email.strip().lower()
        users = cls.get_all_users()
        for user in users:
            if user.email.lower() == email_lower:
                return user
        return None

    # ────────────────────────────────────────────
    #  Profile update
    # ────────────────────────────────────────────

    @classmethod
    def update_user(cls, user_id: str, name: Optional[str] = None, email: Optional[str] = None,
                    skills: Optional[List[str]] = None, resume: Optional[str] = None) -> Optional[User]:
        """Updates the data of an existing candidate. Only provided (non-None) fields are updated."""
        users = cls.get_all_users()
        user_updated = False

        for user in users:
            if user.id == user_id:
                if name is not None:
                    user.name = validate_not_empty(name, "name")
                if email is not None:
                    email_clean = email.strip().lower()
                    if not validate_email(email_clean):
                        raise ValueError("The email address does not have a valid format.")
                    existing = cls.get_user_by_email(email_clean)
                    if existing and existing.id != user_id:
                        raise ValueError(f"The email '{email_clean}' is already in use.")
                    user.email = email_clean
                if skills is not None:
                    user.skills = validate_skills(skills)
                if resume is not None:
                    user.resume = validate_not_empty(resume, "professional summary")
                user_updated = True
                break

        if user_updated:
            users_data = [u.to_dict() for u in users]
            cls._save_all_users_data(users_data)
            return cls.get_user_by_id(user_id)
        return None

    # ────────────────────────────────────────────
    #  Search
    # ────────────────────────────────────────────

    @classmethod
    def search_by_skill(cls, skill: str) -> List[User]:
        """Searches for candidates who have a specific skill (case-insensitive)."""
        if not skill or not skill.strip():
            return []
        skill_lower = skill.strip().lower()
        users = cls.get_all_users()
        return [user for user in users if any(s.lower() == skill_lower for s in user.skills)]

    @classmethod
    def search_by_name(cls, name: str) -> List[User]:
        """Searches for candidates whose name contains the given text (case-insensitive)."""
        if not name or not name.strip():
            return []
        name_lower = name.strip().lower()
        users = cls.get_all_users()
        return [user for user in users if name_lower in user.name.lower()]

    # ────────────────────────────────────────────
    #  Deletion
    # ────────────────────────────────────────────

    @classmethod
    def delete_user(cls, user_id: str) -> bool:
        """Deletes a candidate from the system by their ID."""
        users_data = cls._get_all_users_data()
        original_count = len(users_data)
        users_data = [u for u in users_data if u.get("id") != user_id]
        if len(users_data) < original_count:
            cls._save_all_users_data(users_data)
            return True
        return False
