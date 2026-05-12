from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List
from datetime import datetime

@dataclass
class Recruiter:
    """
    Representa a una Entidad Empleadora en JobConnect.
    Gestiona el inventario de vacantes y la identidad corporativa.
    """
    company_name: str
    tax_id: str  # Identificador fiscal (NIT/RUT/RFC)
    industry_sector: str
    contact_email: str
    id: UUID = field(default_factory=uuid4)
    job_postings_ids: List[UUID] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def add_job_posting(self, job_id: UUID) -> None:
        """Registra una nueva vacante bajo la autoría de este empleador."""
        if job_id not in self.job_postings_ids:
            self.job_postings_ids.append(job_id)

    def remove_job_posting(self, job_id: UUID) -> bool:
        """Elimina una vacante del inventario del empleador."""
        if job_id in self.job_postings_ids:
            self.job_postings_ids.remove(job_id)
            return True
        return False

    def to_dict(self) -> dict:

        return {
            "id": str(self.id),
            "company_name": self.company_name,
            "tax_id": self.tax_id,
            "industry_sector": self.industry_sector,
            "contact_email": self.contact_email,
            "job_postings_ids": [str(jid) for jid in self.job_postings_ids],
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }