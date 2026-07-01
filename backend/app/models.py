from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ===========================
# User Registration Model
# ===========================
class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    created_at: datetime = datetime.utcnow()


# ===========================
# Login Model
# ===========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ===========================
# Subscription Model
# ===========================
class Subscription(BaseModel):
    subscription_name: str
    category: str
    amount: float
    currency: str
    renewal_date: str
    reminder_days: int
    notes: Optional[str] = ""
    reminder_sent: bool = False
    created_at: datetime = datetime.utcnow()


# ===========================
# Update Subscription Model
# ===========================
class UpdateSubscription(BaseModel):
    subscription_name: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    renewal_date: Optional[str] = None
    reminder_days: Optional[int] = None
    notes: Optional[str] = None