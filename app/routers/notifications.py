from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.notification import Notification
from app.core.auth import require_admin

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_notifications(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    notifications = db.query(Notification).order_by(Notification.created_at.desc()).all()
    return [
        {
            "id": n.id,
            "message": n.message,
            "type": n.type,
            "created_at": n.created_at,
            "is_read": n.is_read
        } for n in notifications
    ] 