from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    prescription_date: date
    medications: str
    dosage_instructions: Optional[str] = None
    duration: Optional[str] = None
    refills_allowed: int = 0
    notes: Optional[str] = None
    status: str = "active"
    created_by: int

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    medications: Optional[str] = None
    dosage_instructions: Optional[str] = None
    duration: Optional[str] = None
    refills_allowed: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class PrescriptionResponse(PrescriptionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 