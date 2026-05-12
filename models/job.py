import uuid
from datetime import datetime
from typing import Optional

class Job:
    """Modelo que representa una vacante de trabajo en el sistema."""
    
    def __init__(self, title: str, description: str, employer_id: str, salary: Optional[float] = None, status: str = "abierta"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.employer_id = employer_id
        self.salary = salary
        self.status = status
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "employer_id": self.employer_id,
            "salary": self.salary,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        job = cls(
            title=data["title"],
            description=data["description"],
            employer_id=data["employer_id"],
            salary=data.get("salary"),
            status=data.get("status", "abierta")
        )
        # Restaurar ID y fecha originales si vienen en el diccionario
        if "id" in data:
            job.id = data["id"]
        if "created_at" in data:
            job.created_at = data["created_at"]
        return job
