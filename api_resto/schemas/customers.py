from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone_number: str

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if len(v) < 10:
            raise ValueError('Phone number must be at least 10 characters')
        if len(v) > 20:
            raise ValueError('Phone number must be 20 characters or less')
        return v

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

class Customer(CustomerBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
