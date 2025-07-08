from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    prescription_date = Column(Date, nullable=False)
    medications = Column(Text, nullable=False)  # JSON string for medication details
    dosage_instructions = Column(Text)
    duration = Column(String(50))  # e.g., "7 days", "2 weeks"
    refills_allowed = Column(Integer, default=0)
    notes = Column(Text)
    status = Column(String(20), default="active")  # active, completed, cancelled
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    created_by_user = relationship("User", back_populates="prescriptions_created", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Prescription(id={self.id}, patient_id={self.patient_id}, prescription_date='{self.prescription_date}')>" 