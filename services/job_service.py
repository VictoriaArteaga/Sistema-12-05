import os
from typing import List, Optional
from models.job import Job
from storage.json_manager import load_data, save_data

class JobService:
    """Service to handle business logic related to jobs."""
    
    FILE_PATH = os.path.join("storage", "data", "jobs.json")

    @classmethod
    def _get_all_jobs_data(cls) -> List[dict]:
        """Helper method to get all jobs as dictionaries."""
        try:
            return load_data(cls.FILE_PATH)
        except Exception:
            return []

    @classmethod
    def _save_all_jobs_data(cls, data: List[dict]) -> None:
        """Helper method to save all jobs dictionaries."""
        save_data(cls.FILE_PATH, data)

    @classmethod
    def create_job(cls, title: str, description: str, employer_id: str, salary: Optional[float] = None) -> Job:
        """Creates a new job and saves it to storage."""
        new_job = Job(title=title, description=description, employer_id=employer_id, salary=salary)
        
        jobs_data = cls._get_all_jobs_data()
        jobs_data.append(new_job.to_dict())
        cls._save_all_jobs_data(jobs_data)
        
        return new_job

    @classmethod
    def get_all_jobs(cls) -> List[Job]:
        """Retrieves a list of all jobs."""
        jobs_data = cls._get_all_jobs_data()
        return [Job.from_dict(data) for data in jobs_data]

    @classmethod
    def get_job_by_id(cls, job_id: str) -> Optional[Job]:
        """Retrieves a specific job by its ID."""
        jobs = cls.get_all_jobs()
        for job in jobs:
            if job.id == job_id:
                return job
        return None

    @classmethod
    def search_jobs(cls, keyword: str) -> List[Job]:
        """Searches for active jobs by keyword in title or description."""
        jobs = cls.get_all_jobs()
        keyword_lower = keyword.lower()
        results = []
        for job in jobs:
            if job.status == "abierta":
                if keyword_lower in job.title.lower() or keyword_lower in job.description.lower():
                    results.append(job)
        return results

    @classmethod
    def close_job(cls, job_id: str, employer_id: str) -> bool:
        """
        Closes a job posting. 
        Business Rule: Only the employer who created the job can close it.
        """
        jobs = cls.get_all_jobs()
        job_updated = False
        
        for job in jobs:
            if job.id == job_id:
                if job.employer_id != employer_id:
                    raise PermissionError("No autorizado: Solo el dueño de la vacante puede cerrarla.")
                if job.status != "abierta":
                    return False # Already closed or not open
                
                job.status = "cerrada"
                job_updated = True
                break
        
        if job_updated:
            jobs_data = [job.to_dict() for job in jobs]
            cls._save_all_jobs_data(jobs_data)
            return True
        return False
