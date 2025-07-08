from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime, timedelta

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Password expiration fields
    password_changed_at = Column(DateTime(timezone=True), server_default=func.now())
    password_expires_at = Column(DateTime(timezone=True), nullable=True)
    force_password_change = Column(Boolean, default=False)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    appointments_created = relationship("Appointment", back_populates="created_by_user", foreign_keys="Appointment.created_by")
    medical_records_created = relationship("MedicalRecord", back_populates="created_by_user", foreign_keys="MedicalRecord.created_by")
    prescriptions_created = relationship("Prescription", back_populates="created_by_user", foreign_keys="Prescription.created_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    def set_password_expiration(self, days: int = 90):
        """Set password expiration date (default 90 days = 3 months)"""
        self.password_changed_at = datetime.utcnow()
        self.password_expires_at = datetime.utcnow() + timedelta(days=days)
        self.force_password_change = False
    
    def is_password_expired(self) -> bool:
        """Check if password has expired"""
        if not self.password_expires_at:
            return False
        return datetime.utcnow() > self.password_expires_at
    
    def days_until_password_expiry(self) -> int:
        """Get number of days until password expires"""
        if not self.password_expires_at:
            return -1
        delta = self.password_expires_at - datetime.utcnow()
        return max(0, delta.days) 