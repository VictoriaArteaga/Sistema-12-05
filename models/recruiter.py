# Modelo que representa un empleador o empresa dentro del sistema JobConnect.
import uuid
from datetime import datetime


class Recruiter:

    def __init__(
        self,
        company_name: str,
        email: str,
        industry: str
    ):
        # ID único del reclutador
        self.id = str(uuid.uuid4())

        # Nombre de la empresa
        self.company_name = company_name

        # Correo de contacto
        self.email = email

        # Sector o industria
        self.industry = industry

        # Fecha de creación
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        
        """
        Convierte el objeto Recruiter en un diccionario
        para poder guardarlo en JSON.
        """

        return {
            "id": self.id,
            "company_name": self.company_name,
            "email": self.email,
            "industry": self.industry,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Recruiter':
        """
        Reconstruye un objeto Recruiter desde un diccionario.
        """

        recruiter = cls(
            company_name=data["company_name"],
            email=data["email"],
            industry=data["industry"]
        )

        # Restaurar datos originales
        if "id" in data:
            recruiter.id = data["id"]

        if "created_at" in data:
            recruiter.created_at = data["created_at"]

        return recruiter