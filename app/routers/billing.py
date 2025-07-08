from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import uuid
from app.core.database import get_db
from app.models.billing import Bill, BillItem, PaymentStatus, PaymentMethod
from app.models.patient import Patient
from app.schemas.billing import (
    BillCreate, 
    BillUpdate, 
    BillResponse, 
    BillItemCreate, 
    BillItemResponse,
    PaymentCreate
)
from app.core.notifications import create_notification
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["billing"])

def generate_bill_number() -> str:
    """Generate a unique bill number"""
    return f"BILL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

@router.get("/", response_model=List[BillResponse])
async def get_bills(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all bills with optional filtering"""
    query = db.query(Bill)
    
    if status:
        query = query.filter(Bill.status == status)
    if patient_id:
        query = query.filter(Bill.patient_id == patient_id)
    
    bills = query.offset(skip).limit(limit).all()
    return bills

@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get a specific bill by ID"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bill not found"
        )
    return bill

@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(bill_data: BillCreate, db: Session = Depends(get_db)):
    """Create a new bill with items"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == bill_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Calculate total amount from items
    total_amount = 0.0
    for item in bill_data.items:
        total_amount += item.quantity * item.unit_price
    
    # Create bill
    bill = Bill(
        bill_number=generate_bill_number(),
        patient_id=bill_data.patient_id,
        bill_date=bill_data.bill_date,
        due_date=bill_data.due_date,
        total_amount=total_amount,
        balance=total_amount,
        status=bill_data.status,
        payment_method=bill_data.payment_method,
        insurance_provider=bill_data.insurance_provider,
        insurance_number=bill_data.insurance_number,
        insurance_coverage=bill_data.insurance_coverage,
        notes=bill_data.notes
    )
    
    db.add(bill)
    db.flush()  # Get the bill ID
    
    # Create bill items
    for item_data in bill_data.items:
        bill_item = BillItem(
            bill_id=bill.id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total_price=item_data.quantity * item_data.unit_price,
            item_type=item_data.item_type
        )
        db.add(bill_item)
    
    db.commit()
    db.refresh(bill)
    return bill

@router.put("/{bill_id}", response_model=BillResponse)
async def update_bill(bill_id: int, bill_update: BillUpdate, db: Session = Depends(get_db)):
    """Update a bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    # Update fields
    update_data = bill_update.dict(exclude_unset=True)
    
    # Handle payment updates
    if 'paid_amount' in update_data:
        new_paid_amount = update_data['paid_amount']
        bill.paid_amount = new_paid_amount  # type: ignore
        bill.balance = bill.total_amount - new_paid_amount  # type: ignore
        
        # Update status based on payment
        if bill.balance <= 0:  # type: ignore
            bill.status = PaymentStatus.PAID  # type: ignore
        elif new_paid_amount > 0:
            bill.status = PaymentStatus.PARTIAL  # type: ignore
    
    # Update other fields
    for field, value in update_data.items():
        if field != 'paid_amount':
            setattr(bill, field, value)
    
    db.commit()
    db.refresh(bill)
    return bill

@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    """Delete a bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    # Check if bill can be deleted (not paid)
    if bill.status == PaymentStatus.PAID:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a paid bill"
        )
    
    db.delete(bill)
    db.commit()
    return None

@router.post("/{bill_id}/pay", response_model=BillResponse)
async def pay_bill(bill_id: int, payment: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Make a payment on a bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )
    
    if bill.status == PaymentStatus.PAID:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bill is already fully paid"
        )
    
    if payment.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than 0"
        )
    
    # Update payment
    bill.paid_amount += payment.amount  # type: ignore
    bill.balance = bill.total_amount - bill.paid_amount  # type: ignore
    bill.payment_method = payment.payment_method  # type: ignore
    
    # Update status
    if bill.balance <= 0:  # type: ignore
        bill.status = PaymentStatus.PAID  # type: ignore
    else:
        bill.status = PaymentStatus.PARTIAL  # type: ignore
    
    db.commit()
    db.refresh(bill)
    
    # Trigger notification for admin
    create_notification(db, f"Bill #{bill.id} paid by {bill.patient_name}", "bill")
    return bill

@router.get("/patient/{patient_id}", response_model=List[BillResponse])
async def get_patient_bills(patient_id: int, db: Session = Depends(get_db)):
    """Get all bills for a specific patient"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    bills = db.query(Bill).filter(Bill.patient_id == patient_id).all()
    return bills 