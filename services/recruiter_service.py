# Servicio de gestión de reclutadores

from models.recruiter import Recruiter
from models.job import Job
from storage.json_manager import JSONManager
from typing import List, Optional


class RecruiterService:
    """Servicio de lógica de negocio para reclutadores."""
    
    def __init__(self):
        self.json_manager = JSONManager()
        self.recruiters_file = "recruiters.json"
        self.jobs_file = "jobs.json"
    
    def create_recruiter(self, company_name: str, email: str, industry: str = "") -> Recruiter:
        # Validar que no exista ya un reclutador con ese email
        if self._email_exists(email):
            raise ValueError(f"Ya existe un reclutador con el email: {email}")
        
        recruiter = Recruiter(company_name, email, industry)
        self.json_manager.append_data(self.recruiters_file, recruiter.to_dict())
        return recruiter
    
    def _email_exists(self, email: str) -> bool:
        """Verifica si un email ya está registrado."""
        recruiters = self.json_manager.find_by_field(self.recruiters_file, "email", email)
        return len(recruiters) > 0
    
    def get_recruiter_by_id(self, recruiter_id: str) -> Optional[Recruiter]:
        data = self.json_manager.find_by_id(self.recruiters_file, recruiter_id)
        if data:
            return Recruiter.from_dict(data)
        return None
    
    def get_all_recruiters(self) -> List[Recruiter]:

        data = self.json_manager.load_data(self.recruiters_file)
        return [Recruiter.from_dict(item) for item in data]
    
    def create_job(self, recruiter_id: str, title: str, description: str, 
                  salary: Optional[float] = None) -> Job:
        # Validar que el reclutador existe
        if not self.get_recruiter_by_id(recruiter_id):
            raise ValueError(f"Reclutador no encontrado: {recruiter_id}")
        
        job = Job(title, description, recruiter_id, salary, status="abierta")
        self.json_manager.append_data(self.jobs_file, job.to_dict())
        return job
    
    def get_recruiter_jobs(self, recruiter_id: str) -> List[Job]:

        data = self.json_manager.find_by_field(self.jobs_file, "employer_id", recruiter_id)
        return [Job.from_dict(item) for item in data]
    
    def close_job(self, recruiter_id: str, job_id: str) -> bool:

        job_data = self.json_manager.find_by_id(self.jobs_file, job_id)
        
        if not job_data:
            raise ValueError(f"Vacante no encontrada: {job_id}")
        
        # Validar que el reclutador es el dueño
        if job_data.get("employer_id") != recruiter_id:
            raise ValueError("No tienes autorización para cerrar esta vacante")
        
        job = Job.from_dict(job_data)
        job.status = "cerrada"
        return self.json_manager.update_data(self.jobs_file, job_id, job.to_dict())
    
    def get_job_applications(self, recruiter_id: str, job_id: str) -> List[dict]:

        job_data = self.json_manager.find_by_id(self.jobs_file, job_id)
        
        if not job_data:
            raise ValueError(f"Vacante no encontrada: {job_id}")
        
        if job_data.get("employer_id") != recruiter_id:
            raise ValueError("No tienes autorización para ver estas aplicaciones")
        
        applications = self.json_manager.find_by_field("applications.json", "job_id", job_id)
        return applications
    
    def update_application_status(self, recruiter_id: str, job_id: str, 
                                 application_id: str, new_status: str) -> bool:
        
        # Verificar que el reclutador es el dueño de la vacante
        job_data = self.json_manager.find_by_id(self.jobs_file, job_id)
        
        if not job_data:
            raise ValueError(f"Vacante no encontrada: {job_id}")
        
        if job_data.get("employer_id") != recruiter_id:
            raise ValueError("No tienes autorización para actualizar esta aplicación")
        
        app_data = self.json_manager.find_by_id("applications.json", application_id)
        
        if not app_data:
            raise ValueError(f"Postulación no encontrada: {application_id}")
        
        app_data["status"] = new_status
        return self.json_manager.update_data("applications.json", application_id, app_data)

