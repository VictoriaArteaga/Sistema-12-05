import os
from typing import List
from models.application import Application
from storage.json_manager import load_data, save_data

class ApplicationService:
    """Service to handle business logic related to applications."""
    
    FILE_PATH = os.path.join("storage", "data", "applications.json")

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
        """Retrieves a list of all applications."""
        apps_data = cls._get_all_applications_data()
        return [Application.from_dict(data) for data in apps_data]

    @classmethod
    def already_applied(cls, candidate_id: str, job_id: str) -> bool:
        """Checks if a candidate has already applied to a specific job."""
        applications = cls.get_all_applications()
        for app in applications:
            if app.candidate_id == candidate_id and app.job_id == job_id:
                return True
        return False

    @classmethod
    def apply_to_job(cls, job_id: str, candidate_id: str) -> Application:
        """
        Creates a new application for a job.
        Business Rule: A candidate cannot apply twice to the same job.
        """
        if cls.already_applied(candidate_id, job_id):
            raise ValueError("Ya aplicaste a esta vacante.")
            
        new_application = Application(job_id=job_id, candidate_id=candidate_id)
        
        apps_data = cls._get_all_applications_data()
        apps_data.append(new_application.to_dict())
        cls._save_all_applications_data(apps_data)
        
        return new_application

    @classmethod
    def get_applications_by_candidate(cls, candidate_id: str) -> List[Application]:
        """Retrieves all applications made by a specific candidate."""
        applications = cls.get_all_applications()
        return [app for app in applications if app.candidate_id == candidate_id]

    @classmethod
    def get_applications_by_job(cls, job_id: str) -> List[Application]:
        """Retrieves all applications for a specific job."""
        applications = cls.get_all_applications()
        return [app for app in applications if app.job_id == job_id]
