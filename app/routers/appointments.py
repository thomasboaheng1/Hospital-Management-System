from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.core.auth import get_current_user
import uuid

router = APIRouter()

@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(db: Session = Depends(get_db)):
    """Get all appointments with patient and doctor information"""
    appointments = db.query(Appointment).all()
    
    result = []
    for appointment in appointments:
        patient = appointment.patient
        doctor = appointment.doctor
        doctor_user = doctor.user if doctor else None
        
        appointment_data = {
            "id": appointment.id,
            "appointment_id": appointment.appointment_id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "duration": appointment.duration,
            "status": appointment.status,
            "reason": appointment.reason,
            "notes": appointment.notes,
            "created_by": appointment.created_by,
            "created_at": appointment.created_at,
            "updated_at": appointment.updated_at,
            "patient_name": f"{patient.first_name} {patient.last_name}" if patient else None,
            "doctor_name": f"Dr. {doctor_user.first_name} {doctor_user.last_name}" if doctor_user else None,
            "appointment_type": appointment.reason or "General"
        }
        result.append(appointment_data)
    
    return result

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Get a specific appointment by ID"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    patient = appointment.patient
    doctor = appointment.doctor
    doctor_user = doctor.user if doctor else None
    
    return {
        "id": appointment.id,
        "appointment_id": appointment.appointment_id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date,
        "appointment_time": appointment.appointment_time,
        "duration": appointment.duration,
        "status": appointment.status,
        "reason": appointment.reason,
        "notes": appointment.notes,
        "created_by": appointment.created_by,
        "created_at": appointment.created_at,
        "updated_at": appointment.updated_at,
        "patient_name": f"{patient.first_name} {patient.last_name}" if patient else None,
        "doctor_name": f"Dr. {doctor_user.first_name} {doctor_user.last_name}" if doctor_user else None,
        "appointment_type": appointment.reason or "General"
    }

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new appointment"""
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Generate unique appointment ID
    appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
    
    db_appointment = Appointment(
        appointment_id=appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        duration=appointment.duration,
        status=appointment.status,
        reason=appointment.reason,
        notes=appointment.notes,
        created_by=current_user.id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    return {
        "id": db_appointment.id,
        "appointment_id": db_appointment.appointment_id,
        "patient_id": db_appointment.patient_id,
        "doctor_id": db_appointment.doctor_id,
        "appointment_date": db_appointment.appointment_date,
        "appointment_time": db_appointment.appointment_time,
        "duration": db_appointment.duration,
        "status": db_appointment.status,
        "reason": db_appointment.reason,
        "notes": db_appointment.notes,
        "created_by": db_appointment.created_by,
        "created_at": db_appointment.created_at,
        "updated_at": db_appointment.updated_at,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "doctor_name": f"Dr. {doctor.user.first_name} {doctor.user.last_name}" if doctor.user else None,
        "appointment_type": db_appointment.reason or "General"
    }

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update an appointment"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    update_data = appointment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    db.commit()
    db.refresh(db_appointment)
    
    patient = db_appointment.patient
    doctor = db_appointment.doctor
    doctor_user = doctor.user if doctor else None
    
    return {
        "id": db_appointment.id,
        "appointment_id": db_appointment.appointment_id,
        "patient_id": db_appointment.patient_id,
        "doctor_id": db_appointment.doctor_id,
        "appointment_date": db_appointment.appointment_date,
        "appointment_time": db_appointment.appointment_time,
        "duration": db_appointment.duration,
        "status": db_appointment.status,
        "reason": db_appointment.reason,
        "notes": db_appointment.notes,
        "created_by": db_appointment.created_by,
        "created_at": db_appointment.created_at,
        "updated_at": db_appointment.updated_at,
        "patient_name": f"{patient.first_name} {patient.last_name}" if patient else None,
        "doctor_name": f"Dr. {doctor_user.first_name} {doctor_user.last_name}" if doctor_user else None,
        "appointment_type": db_appointment.reason or "General"
    }

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete an appointment"""
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"} 