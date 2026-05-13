# Modelo de reclutador

import uuid
from datetime import datetime
from typing import Optional

class Recruiter:
    """Modelo que representa un reclutador/empresa en el sistema."""

    def __init__(self, company_name: str, email: str, industry: str = ""):
        self.id = str(uuid.uuid4())
        self.company_name = company_name
        self.email = email
        self.industry = industry
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "company_name": self.company_name,
            "email": self.email,
            "industry": self.industry,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Recruiter':
        recruiter = cls(
            company_name=data["company_name"],
            email=data["email"],
            industry=data.get("industry", "")
        )
        # Restaurar ID y fecha originales si vienen en el diccionario
        if "id" in data:
            recruiter.id = data["id"]
        if "created_at" in data:
            recruiter.created_at = data["created_at"]
        return recruiter
