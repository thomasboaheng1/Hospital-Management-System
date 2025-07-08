from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DoctorBase(BaseModel):
    specialization: str
    license_number: str
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = 0.0
    education: Optional[str] = None
    certifications: Optional[str] = None
    bio: Optional[str] = None

class DoctorCreate(DoctorBase):
    user_id: int

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    education: Optional[str] = None
    certifications: Optional[str] = None
    bio: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Include user information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    department: Optional[str] = None

    class Config:
        from_attributes = True 