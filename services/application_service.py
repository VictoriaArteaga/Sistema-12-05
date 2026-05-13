import os
from typing import List, Optional
from models.application import Application
from storage.json_manager import load_data, save_data
from utils.validators import validate_not_empty, validate_status


class ApplicationService:
    """Service to manage job applications (postulations)."""

    FILE_PATH = os.path.join("storage", "data", "applications.json")
    VALID_STATUSES = ["pendiente", "revisada", "aceptada", "rechazada", "retirada"]

    @classmethod
    def _get_all_applications_data(cls) -> List[dict]:
        """Helper method to get all applications as dictionaries."""
        try:
            return load_data(cls.FILE_PATH)
        except Exception:
            return []

    @classmethod
    def _save_all_applications_data(cls, data: List[dict]) -> None:
        """Helper method to save all applications dictionaries."""
        save_data(cls.FILE_PATH, data)

    @classmethod
    def get_all_applications(cls) -> List[Application]:
        """Returns all applications."""
        apps_data = cls._get_all_applications_data()
        return [Application.from_dict(data) for data in apps_data]

    @classmethod
    def get_application_by_id(cls, application_id: str) -> Optional[Application]:
        """Finds an application by its ID."""
        applications = cls.get_all_applications()
        for app in applications:
            if app.id == application_id:
                return app
        return None

    @classmethod
    def get_applications_by_candidate(cls, candidate_id: str) -> List[Application]:
        """Returns all applications made by a specific candidate."""
        applications = cls.get_all_applications()
        return [app for app in applications if app.candidate_id == candidate_id]

    @classmethod
    def get_applications_by_job(cls, job_id: str) -> List[Application]:
        """Returns all applications for a specific job."""
        applications = cls.get_all_applications()
        return [app for app in applications if app.job_id == job_id]

    @classmethod
    def already_applied(cls, candidate_id: str, job_id: str) -> bool:
        """Checks if a candidate has already applied to a specific job (excludes withdrawn)."""
        applications = cls.get_all_applications()
        for app in applications:
            if app.candidate_id == candidate_id and app.job_id == job_id:
                if app.status != "retirada":
                    return True
        return False

    @classmethod
    def apply_to_job(cls, job_id: str, candidate_id: str) -> Application:
        """
        Creates a new application for a job.
        Business rule: A candidate cannot apply twice to the same job.
        """
        job_id = validate_not_empty(job_id, "job ID")
        candidate_id = validate_not_empty(candidate_id, "candidate ID")

        if cls.already_applied(candidate_id, job_id):
            raise ValueError("You have already applied to this job.")

        new_application = Application(job_id=job_id, candidate_id=candidate_id)
        apps_data = cls._get_all_applications_data()
        apps_data.append(new_application.to_dict())
        cls._save_all_applications_data(apps_data)
        return new_application

    @classmethod
    def update_application_status(cls, application_id: str, new_status: str) -> Optional[Application]:
        """Updates the status of an application. Valid: pendiente, revisada, aceptada, rechazada, retirada."""
        new_status = validate_status(new_status, cls.VALID_STATUSES)
        applications = cls.get_all_applications()
        app_updated = False
        for app in applications:
            if app.id == application_id:
                app.status = new_status
                app_updated = True
                break
        if app_updated:
            apps_data = [a.to_dict() for a in applications]
            cls._save_all_applications_data(apps_data)
            return cls.get_application_by_id(application_id)
        return None

    @classmethod
    def withdraw_application(cls, application_id: str, candidate_id: str) -> bool:
        """
        Withdraws an application (marks it as 'retirada').
        Business rule: Only the candidate who applied can withdraw it.
        """
        applications = cls.get_all_applications()
        app_updated = False
        for app in applications:
            if app.id == application_id:
                if app.candidate_id != candidate_id:
                    raise PermissionError("Unauthorized: You can only withdraw your own applications.")
                if app.status in ("aceptada", "rechazada"):
                    raise ValueError(f"Cannot withdraw an application with status '{app.status}'.")
                if app.status == "retirada":
                    return False
                app.status = "retirada"
                app_updated = True
                break
        if app_updated:
            apps_data = [a.to_dict() for a in applications]
            cls._save_all_applications_data(apps_data)
            return True
        return False

    @classmethod
    def get_applications_by_status(cls, status: str) -> List[Application]:
        """Filters applications by status."""
        status_lower = status.strip().lower() if status else ""
        applications = cls.get_all_applications()
        return [app for app in applications if app.status == status_lower]

    @classmethod
    def get_pending_applications_for_job(cls, job_id: str) -> List[Application]:
        """Returns pending applications for a specific job."""
        applications = cls.get_applications_by_job(job_id)
        return [app for app in applications if app.status == "pendiente"]

    @classmethod
    def count_applications_for_job(cls, job_id: str) -> int:
        """Counts active (non-withdrawn) applications for a job."""
        applications = cls.get_applications_by_job(job_id)
        return len([app for app in applications if app.status != "retirada"])
