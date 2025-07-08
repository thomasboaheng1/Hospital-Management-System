from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    record_date = Column(Date, nullable=False)
    diagnosis = Column(Text)
    symptoms = Column(Text)
    treatment_plan = Column(Text)
    medications = Column(Text)
    test_results = Column(Text)
    vital_signs = Column(Text)  # JSON string for blood pressure, temperature, etc.
    notes = Column(Text)
    follow_up_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")
    created_by_user = relationship("User", back_populates="medical_records_created", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<MedicalRecord(id={self.id}, patient_id={self.patient_id}, record_date='{self.record_date}')>" 