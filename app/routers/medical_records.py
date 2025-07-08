from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse

router = APIRouter()

@router.get("/", response_model=List[MedicalRecordResponse])
async def get_medical_records(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all medical records with optional filtering"""
    query = db.query(MedicalRecord)
    
    if patient_id:
        query = query.filter(MedicalRecord.patient_id == patient_id)
    if doctor_id:
        query = query.filter(MedicalRecord.doctor_id == doctor_id)
    
    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    """Get a specific medical record by ID"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    return record

@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(record_data: MedicalRecordCreate, db: Session = Depends(get_db)):
    """Create a new medical record"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == record_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == record_data.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Create medical record
    record = MedicalRecord(
        patient_id=record_data.patient_id,
        doctor_id=record_data.doctor_id,
        record_date=record_data.record_date,
        diagnosis=record_data.diagnosis,
        symptoms=record_data.symptoms,
        treatment_plan=record_data.treatment_plan,
        medications=record_data.medications,
        test_results=record_data.test_results,
        vital_signs=record_data.vital_signs,
        notes=record_data.notes,
        follow_up_date=record_data.follow_up_date,
        created_by=record_data.created_by
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_medical_record(
    record_id: int, 
    record_update: MedicalRecordUpdate, 
    db: Session = Depends(get_db)
):
    """Update a medical record"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    # Update fields
    update_data = record_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a medical record"""
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    
    db.delete(record)
    db.commit()
    return None

@router.get("/patient/{patient_id}", response_model=List[MedicalRecordResponse])
async def get_patient_medical_records(patient_id: int, db: Session = Depends(get_db)):
    """Get all medical records for a specific patient"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    records = db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()
    return records 