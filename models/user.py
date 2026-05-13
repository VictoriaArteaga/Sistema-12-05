# Modelo de usuario

import uuid
from datetime import datetime
from typing import List, Optional

class User:
    """Modelo que representa un usuario/candidato en el sistema."""

    def __init__(self, name: str, email: str, skills: Optional[List[str]] = None, resume: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.skills = skills or []
        self.resume = resume
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
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
        user = cls(
            name=data["name"],
            email=data["email"],
            skills=data.get("skills", []),
            resume=data.get("resume", "")
        )
        # Restaurar ID y fecha originales si vienen en el diccionario
        if "id" in data:
            user.id = data["id"]
        if "created_at" in data:
            user.created_at = data["created_at"]
        return user
