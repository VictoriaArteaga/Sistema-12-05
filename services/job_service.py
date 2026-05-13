import os
from typing import List, Optional
from models.job import Job
from storage.json_manager import load_data, save_data
from utils.validators import validate_not_empty, validate_salary, validate_status


class JobService:
    """Service to manage job postings."""

    FILE_PATH = os.path.join("storage", "data", "jobs.json")
    VALID_STATUSES = ["abierta", "cerrada"]

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
        """Creates a new job posting and saves it to storage."""
        title = validate_not_empty(title, "job title")
        description = validate_not_empty(description, "job description")
        employer_id = validate_not_empty(employer_id, "employer ID")
        salary = validate_salary(salary)

        new_job = Job(title=title, description=description, employer_id=employer_id, salary=salary)
        jobs_data = cls._get_all_jobs_data()
        jobs_data.append(new_job.to_dict())
        cls._save_all_jobs_data(jobs_data)
        return new_job

    @classmethod
    def get_all_jobs(cls) -> List[Job]:
        """Returns all job postings."""
        jobs_data = cls._get_all_jobs_data()
        return [Job.from_dict(data) for data in jobs_data]

    @classmethod
    def get_open_jobs(cls) -> List[Job]:
        """Returns only open job postings."""
        jobs = cls.get_all_jobs()
        return [job for job in jobs if job.status == "abierta"]

    @classmethod
    def get_job_by_id(cls, job_id: str) -> Optional[Job]:
        """Finds a job posting by its ID."""
        jobs = cls.get_all_jobs()
        for job in jobs:
            if job.id == job_id:
                return job
        return None

    @classmethod
    def get_jobs_by_employer(cls, employer_id: str) -> List[Job]:
        """Returns all job postings published by a specific employer."""
        jobs = cls.get_all_jobs()
        return [job for job in jobs if job.employer_id == employer_id]

    @classmethod
    def search_jobs(cls, keyword: str) -> List[Job]:
        """Searches for open jobs by keyword in title or description."""
        if not keyword or not keyword.strip():
            return []
        jobs = cls.get_all_jobs()
        keyword_lower = keyword.strip().lower()
        results = []
        for job in jobs:
            if job.status == "abierta":
                if keyword_lower in job.title.lower() or keyword_lower in job.description.lower():
                    results.append(job)
        return results

    @classmethod
    def search_jobs_by_salary_range(cls, min_salary: Optional[float] = None, max_salary: Optional[float] = None) -> List[Job]:
        """Searches for open jobs within a salary range."""
        jobs = cls.get_open_jobs()
        results = []
        for job in jobs:
            if job.salary is None:
                continue
            if min_salary is not None and job.salary < min_salary:
                continue
            if max_salary is not None and job.salary > max_salary:
                continue
            results.append(job)
        return results

    @classmethod
    def update_job(cls, job_id: str, employer_id: str, title: Optional[str] = None, description: Optional[str] = None, salary: Optional[float] = None) -> Optional[Job]:
        """Updates job data. Only the owner can modify it."""
        jobs = cls.get_all_jobs()
        job_updated = False
        for job in jobs:
            if job.id == job_id:
                if job.employer_id != employer_id:
                    raise PermissionError("Unauthorized: Only the job owner can modify it.")
                if job.status == "cerrada":
                    raise ValueError("Cannot modify a closed job posting.")
                if title is not None:
                    job.title = validate_not_empty(title, "job title")
                if description is not None:
                    job.description = validate_not_empty(description, "job description")
                if salary is not None:
                    job.salary = validate_salary(salary)
                job_updated = True
                break
        if job_updated:
            jobs_data = [j.to_dict() for j in jobs]
            cls._save_all_jobs_data(jobs_data)
            return cls.get_job_by_id(job_id)
        return None

    @classmethod
    def close_job(cls, job_id: str, employer_id: str) -> bool:
        """Closes a job posting. Only the owner can close it."""
        jobs = cls.get_all_jobs()
        job_updated = False
        for job in jobs:
            if job.id == job_id:
                if job.employer_id != employer_id:
                    raise PermissionError("Unauthorized: Only the job owner can close it.")
                if job.status != "abierta":
                    return False
                job.status = "cerrada"
                job_updated = True
                break
        if job_updated:
            jobs_data = [job.to_dict() for job in jobs]
            cls._save_all_jobs_data(jobs_data)
            return True
        return False

    @classmethod
    def reopen_job(cls, job_id: str, employer_id: str) -> bool:
        """Reopens a previously closed job posting. Only the owner can reopen it."""
        jobs = cls.get_all_jobs()
        job_updated = False
        for job in jobs:
            if job.id == job_id:
                if job.employer_id != employer_id:
                    raise PermissionError("Unauthorized: Only the job owner can reopen it.")
                if job.status != "cerrada":
                    return False
                job.status = "abierta"
                job_updated = True
                break
        if job_updated:
            jobs_data = [j.to_dict() for j in jobs]
            cls._save_all_jobs_data(jobs_data)
            return True
        return False

    @classmethod
    def delete_job(cls, job_id: str, employer_id: str) -> bool:
        """Deletes a job posting. Only the owner can delete it."""
        jobs = cls.get_all_jobs()
        target_job = None
        for job in jobs:
            if job.id == job_id:
                target_job = job
                break
        if target_job is None:
            return False
        if target_job.employer_id != employer_id:
            raise PermissionError("Unauthorized: Only the job owner can delete it.")
        jobs_data = [j.to_dict() for j in jobs if j.id != job_id]
        cls._save_all_jobs_data(jobs_data)
        return True
