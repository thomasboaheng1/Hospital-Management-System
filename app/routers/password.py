from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user, get_password_hash, pwd_context
from app.models.user import User

router = APIRouter()

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class PasswordExpiryResponse(BaseModel):
    is_expired: bool
    days_until_expiry: int
    password_expires_at: Optional[datetime]
    force_change: bool

@router.post("/change")
async def change_password(
    password_data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    
    # Verify current password
    if not pwd_context.verify(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Check if new password matches confirmation
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match"
        )
    
    # Check if new password is different from current
    if pwd_context.verify(password_data.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    # Validate password strength (minimum 8 characters, at least one uppercase, one lowercase, one digit)
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    if not any(c.isupper() for c in password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )
    
    if not any(c.islower() for c in password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )
    
    if not any(c.isdigit() for c in password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one digit"
        )
    
    # Hash new password and update user
    new_password_hash = get_password_hash(password_data.new_password)
    current_user.password_hash = new_password_hash
    
    # Set new password expiration (90 days from now)
    current_user.set_password_expiration(90)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Password changed successfully",
        "password_expires_at": current_user.password_expires_at,
        "days_until_expiry": current_user.days_until_password_expiry()
    }

@router.get("/expiry")
async def get_password_expiry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PasswordExpiryResponse:
    """Get password expiry information"""
    
    return PasswordExpiryResponse(
        is_expired=current_user.is_password_expired(),
        days_until_expiry=current_user.days_until_password_expiry(),
        password_expires_at=current_user.password_expires_at,
        force_change=current_user.force_password_change
    )

@router.post("/force-change")
async def force_password_change(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Force a user to change their password (admin only)"""
    
    # Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can force password changes"
        )
    
    # Find target user
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Force password change
    target_user.force_password_change = True
    db.commit()
    
    return {
        "message": f"User {target_user.username} will be required to change password on next login"
    }

@router.post("/reset-expiry")
async def reset_password_expiry(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reset password expiry for a user (admin only)"""
    
    # Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can reset password expiry"
        )
    
    # Find target user
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Reset password expiry
    target_user.set_password_expiration(90)
    target_user.force_password_change = False
    db.commit()
    
    return {
        "message": f"Password expiry reset for user {target_user.username}",
        "password_expires_at": target_user.password_expires_at
    } 