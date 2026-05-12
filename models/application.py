import uuid
from datetime import datetime

class Application:
    """Modelo que representa una postulación de un candidato a una vacante."""
    
    def __init__(self, job_id: str, candidate_id: str, status: str = "pendiente"):
        self.id = str(uuid.uuid4())
        self.job_id = job_id
        self.candidate_id = candidate_id
        self.status = status
        self.applied_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "candidate_id": self.candidate_id,
            "status": self.status,
            "applied_at": self.applied_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Application':
        application = cls(
            job_id=data["job_id"],
            candidate_id=data["candidate_id"],
            status=data.get("status", "pendiente")
        )
        # Restaurar ID y fecha originales si vienen en el diccionario
        if "id" in data:
            application.id = data["id"]
        if "applied_at" in data:
            application.applied_at = data["applied_at"]
        return application
