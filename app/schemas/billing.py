from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from app.models.billing import PaymentStatus, PaymentMethod

class BillItemBase(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float
    item_type: Optional[str] = None

class BillItemCreate(BillItemBase):
    pass

class BillItemResponse(BillItemBase):
    id: int
    bill_id: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True

class BillBase(BaseModel):
    patient_id: int
    bill_date: date
    due_date: Optional[date] = None
    total_amount: float = 0.0
    paid_amount: float = 0.0
    balance: float = 0.0
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method: Optional[PaymentMethod] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_coverage: float = 0.0
    notes: Optional[str] = None

class BillCreate(BillBase):
    items: List[BillItemCreate] = []

class BillUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    paid_amount: Optional[float] = None
    payment_method: Optional[PaymentMethod] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_coverage: Optional[float] = None
    notes: Optional[str] = None
    due_date: Optional[date] = None

class BillResponse(BillBase):
    id: int
    bill_number: str
    items: List[BillItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    amount: float
    payment_method: PaymentMethod 