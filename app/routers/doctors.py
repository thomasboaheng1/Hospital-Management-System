from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.doctor import Doctor
from app.models.user import User, UserRole
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.core.auth import get_current_user, get_password_hash
from app.core.notifications import create_notification

router = APIRouter()

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors(db: Session = Depends(get_db)):
    """Get all doctors with their user information"""
    doctors = db.query(Doctor).all()
    
    result = []
    for doctor in doctors:
        user = doctor.user
        doctor_data = {
            "id": doctor.id,
            "user_id": doctor.user_id,
            "specialization": doctor.specialization,
            "license_number": doctor.license_number,
            "experience_years": doctor.experience_years,
            "consultation_fee": doctor.consultation_fee,
            "education": doctor.education,
            "certifications": doctor.certifications,
            "bio": doctor.bio,
            "created_at": doctor.created_at,
            "updated_at": doctor.updated_at,
            "first_name": user.first_name if user else None,
            "last_name": user.last_name if user else None,
            "email": user.email if user else None,
            "phone": user.phone if user else None,
            "is_active": user.is_active if user else True,
            "department": doctor.specialization  # Using specialization as department for now
        }
        result.append(doctor_data)
    
    return result

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get a specific doctor by ID"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    user = doctor.user
    return {
        "id": doctor.id,
        "user_id": doctor.user_id,
        "specialization": doctor.specialization,
        "license_number": doctor.license_number,
        "experience_years": doctor.experience_years,
        "consultation_fee": doctor.consultation_fee,
        "education": doctor.education,
        "certifications": doctor.certifications,
        "bio": doctor.bio,
        "created_at": doctor.created_at,
        "updated_at": doctor.updated_at,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None,
        "email": user.email if user else None,
        "phone": user.phone if user else None,
        "is_active": user.is_active if user else True,
        "department": doctor.specialization
    }

@router.post("/", response_model=DoctorResponse)
async def create_doctor(doctor_data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new doctor with user account"""
    try:
        # Extract user data from the request
        user_data = {
            "username": doctor_data.get("username"),
            "email": doctor_data.get("email"),
            "password": doctor_data.get("password"),
            "first_name": doctor_data.get("first_name"),
            "last_name": doctor_data.get("last_name"),
            "phone": doctor_data.get("phone"),
            "role": UserRole.DOCTOR
        }
        
        # Check if username or email already exists
        existing_user = db.query(User).filter(
            (User.username == user_data["username"]) | (User.email == user_data["email"])
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data["password"])
        db_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=hashed_password,
            role=user_data["role"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"]
        )
        
        # Set password expiration (90 days from now)
        db_user.set_password_expiration(90)
        
        db.add(db_user)
        db.flush()  # Get the user ID without committing
        
        # Check if license number already exists
        existing_doctor = db.query(Doctor).filter(Doctor.license_number == doctor_data["license_number"]).first()
        if existing_doctor:
            db.rollback()
            raise HTTPException(status_code=400, detail="License number already exists")
        
        # Create doctor
        db_doctor = Doctor(
            user_id=db_user.id,
            specialization=doctor_data["specialization"],
            license_number=doctor_data["license_number"],
            experience_years=doctor_data.get("experience_years"),
            consultation_fee=doctor_data.get("consultation_fee", 0.0),
            education=doctor_data.get("education"),
            certifications=doctor_data.get("certifications"),
            bio=doctor_data.get("bio")
        )
        
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        db.refresh(db_user)
        
        # Trigger notification for admin
        create_notification(db, f"New doctor added: {db_user.first_name} {db_user.last_name}", "doctor")
        
        return {
            "id": db_doctor.id,
            "user_id": db_doctor.user_id,
            "specialization": db_doctor.specialization,
            "license_number": db_doctor.license_number,
            "experience_years": db_doctor.experience_years,
            "consultation_fee": db_doctor.consultation_fee,
            "education": db_doctor.education,
            "certifications": db_doctor.certifications,
            "bio": db_doctor.bio,
            "created_at": db_doctor.created_at,
            "updated_at": db_doctor.updated_at,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "email": db_user.email,
            "phone": db_user.phone,
            "is_active": db_user.is_active,
            "department": db_doctor.specialization
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating doctor: {str(e)}")

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update a doctor"""
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    update_data = doctor.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_doctor, field, value)
    
    db.commit()
    db.refresh(db_doctor)
    
    user = db_doctor.user
    return {
        "id": db_doctor.id,
        "user_id": db_doctor.user_id,
        "specialization": db_doctor.specialization,
        "license_number": db_doctor.license_number,
        "experience_years": db_doctor.experience_years,
        "consultation_fee": db_doctor.consultation_fee,
        "education": db_doctor.education,
        "certifications": db_doctor.certifications,
        "bio": db_doctor.bio,
        "created_at": db_doctor.created_at,
        "updated_at": db_doctor.updated_at,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None,
        "email": user.email if user else None,
        "phone": user.phone if user else None,
        "is_active": user.is_active if user else True,
        "department": db_doctor.specialization
    }

@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a doctor"""
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}

@router.get("/me", response_model=DoctorResponse)
async def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get current doctor's profile"""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    return {
        "id": doctor.id,
        "user_id": doctor.user_id,
        "specialization": doctor.specialization,
        "license_number": doctor.license_number,
        "experience_years": doctor.experience_years,
        "consultation_fee": doctor.consultation_fee,
        "education": doctor.education,
        "certifications": doctor.certifications,
        "bio": doctor.bio,
        "created_at": doctor.created_at,
        "updated_at": doctor.updated_at,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "is_active": current_user.is_active,
        "department": doctor.specialization
    }

@router.get("/me/patients", response_model=List[dict])
async def get_my_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get patients assigned to the current doctor"""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    # Get patients who have appointments with this doctor
    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor.id).all()
    patient_ids = list(set([app.patient_id for app in appointments]))
    
    patients = db.query(Patient).filter(Patient.id.in_(patient_ids)).all()
    
    result = []
    for patient in patients:
        # Get appointment count for this patient
        appointment_count = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.patient_id == patient.id
        ).count()
        
        # Get last appointment
        last_appointment = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.patient_id == patient.id
        ).order_by(Appointment.appointment_date.desc()).first()
        
        patient_data = {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "phone": patient.phone,
            "date_of_birth": patient.date_of_birth,
            "gender": patient.gender,
            "address": patient.address,
            "emergency_contact": patient.emergency_contact,
            "medical_history": patient.medical_history,
            "allergies": patient.allergies,
            "created_at": patient.created_at,
            "updated_at": patient.updated_at,
            "appointment_count": appointment_count,
            "last_appointment": last_appointment.appointment_date if last_appointment else None
        }
        result.append(patient_data)
    
    return result

@router.get("/me/appointments", response_model=List[dict])
async def get_my_appointments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get appointments for the current doctor"""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor.id).all()
    
    result = []
    for appointment in appointments:
        patient = appointment.patient
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
            "patient_email": patient.email if patient else None,
            "patient_phone": patient.phone if patient else None,
            "appointment_type": appointment.reason or "General"
        }
        result.append(appointment_data)
    
    return result

@router.get("/me/medical-records", response_model=List[dict])
async def get_my_medical_records(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get medical records created by the current doctor"""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    records = db.query(MedicalRecord).filter(MedicalRecord.doctor_id == doctor.id).all()
    
    result = []
    for record in records:
        patient = record.patient
        record_data = {
            "id": record.id,
            "patient_id": record.patient_id,
            "doctor_id": record.doctor_id,
            "record_date": record.record_date,
            "diagnosis": record.diagnosis,
            "symptoms": record.symptoms,
            "treatment_plan": record.treatment_plan,
            "medications": record.medications,
            "test_results": record.test_results,
            "vital_signs": record.vital_signs,
            "notes": record.notes,
            "follow_up_date": record.follow_up_date,
            "created_by": record.created_by,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
            "patient_name": f"{patient.first_name} {patient.last_name}" if patient else None,
            "patient_email": patient.email if patient else None
        }
        result.append(record_data)
    
    return result

@router.get("/me/prescriptions", response_model=List[dict])
async def get_my_prescriptions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get prescriptions created by the current doctor"""
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    prescriptions = db.query(Prescription).filter(Prescription.doctor_id == doctor.id).all()
    
    result = []
    for prescription in prescriptions:
        patient = prescription.patient
        prescription_data = {
            "id": prescription.id,
            "patient_id": prescription.patient_id,
            "doctor_id": prescription.doctor_id,
            "medication": prescription.medication,
            "dosage": prescription.dosage,
            "frequency": prescription.frequency,
            "duration": prescription.duration,
            "instructions": prescription.instructions,
            "created_at": prescription.created_at,
            "updated_at": prescription.updated_at,
            "patient_name": f"{patient.first_name} {patient.last_name}" if patient else None,
            "patient_email": patient.email if patient else None
        }
        result.append(prescription_data)
    
    return result 