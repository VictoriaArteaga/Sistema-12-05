from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime


@dataclass
class User:
    """
    Representa a un Candidato dentro de la plataforma JobConnect.
    Incluye perfil profesional, competencias y trazabilidad de aplicaciones...
    """
    first_name: str
    last_name: str
    email: str
    summary: str
    skills: List[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    applied_jobs_ids: List[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del candidato."""
        return f"{self.first_name} {self.last_name}"

    def add_skill(self, skill: str) -> None:
        """Agrega una competencia al catálogo si no existe."""
        clean_skill = skill.strip().capitalize()
        if clean_skill and clean_skill not in self.skills:
            self.skills.append(clean_skill)

    def register_application(self, job_id: UUID) -> None:
        """
        Vincula el ID de una vacante al historial del usuario.
        La validación de unicidad se maneja en la lógica de negocio (Fase II).
        """
        if job_id not in self.applied_jobs_ids:
            self.applied_jobs_ids.append(job_id)

    def to_dict(self) -> dict:

        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "email": self.email,
            "summary": self.summary,
            "skills": self.skills,
            "applied_jobs_ids": [str(jid) for jid in self.applied_jobs_ids],
            "created_at": self.created_at.isoformat()
        }