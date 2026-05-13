# Servicio de gestión de usuarios
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
        """
        Crea un nuevo reclutador/empresa y lo guarda en el sistema.
        
        Args:
            company_name: Nombre de la empresa
            email: Email de la empresa
            industry: Industria (opcional)
        
        Returns:
            Recruiter: El objeto reclutador creado
        """
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
        """
        Obtiene un reclutador por su ID.
        
        Args:
            recruiter_id: ID del reclutador
        
        Returns:
            Recruiter o None si no existe
        """
        data = self.json_manager.find_by_id(self.recruiters_file, recruiter_id)
        if data:
            return Recruiter.from_dict(data)
        return None
    
    def get_all_recruiters(self) -> List[Recruiter]:
        """
        Obtiene todos los reclutadores registrados.
        
        Returns:
            Lista de objetos Recruiter
        """
        data = self.json_manager.load_data(self.recruiters_file)
        return [Recruiter.from_dict(item) for item in data]
    
    def create_job(self, recruiter_id: str, title: str, description: str, 
                  salary: Optional[float] = None) -> Job:
        """
        Crea una nueva vacante (solo el reclutador puede crear).
        
        Args:
            recruiter_id: ID del reclutador que crea la vacante
            title: Título del puesto
            description: Descripción del puesto
            salary: Salario (opcional)
        
        Returns:
            Job: El objeto vacante creado
        
        Raises:
            ValueError: Si el reclutador no existe
        """
        # Validar que el reclutador existe
        if not self.get_recruiter_by_id(recruiter_id):
            raise ValueError(f"Reclutador no encontrado: {recruiter_id}")
        
        job = Job(title, description, recruiter_id, salary, status="abierta")
        self.json_manager.append_data(self.jobs_file, job.to_dict())
        return job
    
    def get_recruiter_jobs(self, recruiter_id: str) -> List[Job]:
        """
        Obtiene todas las vacantes creadas por un reclutador.
        
        Args:
            recruiter_id: ID del reclutador
        
        Returns:
            Lista de objetos Job
        """
        data = self.json_manager.find_by_field(self.jobs_file, "employer_id", recruiter_id)
        return [Job.from_dict(item) for item in data]
    
    def close_job(self, recruiter_id: str, job_id: str) -> bool:
        """
        Cierra una vacante (solo el dueño puede cerrarla).
        
        Args:
            recruiter_id: ID del reclutador que cierra
            job_id: ID de la vacante a cerrar
        
        Returns:
            bool: True si se cerró exitosamente
        
        Raises:
            ValueError: Si el reclutador no es el dueño de la vacante
        """
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
        """
        Obtiene todas las postulaciones para una vacante (solo el dueño).
        
        Args:
            recruiter_id: ID del reclutador
            job_id: ID de la vacante
        
        Returns:
            Lista de postulaciones (aplicaciones)
        
        Raises:
            ValueError: Si el reclutador no es el dueño de la vacante
        """
        job_data = self.json_manager.find_by_id(self.jobs_file, job_id)
        
        if not job_data:
            raise ValueError(f"Vacante no encontrada: {job_id}")
        
        if job_data.get("employer_id") != recruiter_id:
            raise ValueError("No tienes autorización para ver estas aplicaciones")
        
        applications = self.json_manager.find_by_field("applications.json", "job_id", job_id)
        return applications
    
    def update_application_status(self, recruiter_id: str, job_id: str, 
                                 application_id: str, new_status: str) -> bool:
        """
        Actualiza el estado de una postulación (solo el dueño de la vacante).
        
        Args:
            recruiter_id: ID del reclutador
            job_id: ID de la vacante
            application_id: ID de la postulación
            new_status: Nuevo estado (aceptada, rechazada, etc.)
        
        Returns:
            bool: True si se actualizó exitosamente
        
        Raises:
            ValueError: Si no tiene autorización
        """
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


class UserService:
    """Servicio de lógica de negocio para candidatos (usuarios)."""
    
    def __init__(self):
        self.json_manager = JSONManager()
        self.users_file = "users.json"
    
    def register_user(self, name: str, email: str, skills: list = None) -> 'User':
        from models.user import User
        # Verificar si ya existe
        existing = self.json_manager.find_by_field(self.users_file, "email", email)
        if existing:
            user = User.from_dict(existing[0])
            user.name = name
            user.skills = skills or []
            self.json_manager.update_data(self.users_file, user.id, user.to_dict())
            return user
        
        user = User(name, email, skills)
        self.json_manager.append_data(self.users_file, user.to_dict())
        return user

    def get_user_by_email(self, email: str) -> Optional['User']:
        from models.user import User
        data = self.json_manager.find_by_field(self.users_file, "email", email)
        if data:
            return User.from_dict(data[0])
        return None

