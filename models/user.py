# Modelo que representa un candidato dentro de la plataforma.


import uuid
from datetime import datetime
from typing import List


class User:

    def __init__(
        self,
        name: str,
        email: str,
        skills: List[str],
        resume: str
    ):
        # ID único del usuario
        self.id = str(uuid.uuid4())

        # Nombre completo
        self.name = name

        # Correo electrónico
        self.email = email

        # Lista de habilidades
        self.skills = skills

        # Resumen profesional
        self.resume = resume

        # Fecha de registro
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """
        Convierte el objeto User en diccionario
        para persistencia JSON.
        """

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "skills": self.skills,
            "resume": self.resume,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Reconstruye un objeto User desde un diccionario.
        """

        user = cls(
            name=data["name"],
            email=data["email"],
            skills=data.get("skills", []),
            resume=data.get("resume", "")
        )

        # Restaurar datos originales
        if "id" in data:
            user.id = data["id"]

        if "created_at" in data:
            user.created_at = data["created_at"]

        return user
