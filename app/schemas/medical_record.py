from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    record_date: date
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications: Optional[str] = None
    test_results: Optional[str] = None
    vital_signs: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    created_by: int

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications: Optional[str] = None
    test_results: Optional[str] = None
    vital_signs: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 