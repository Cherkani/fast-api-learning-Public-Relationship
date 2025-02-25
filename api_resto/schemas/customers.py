from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional
import re

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone_number: str

    @field_validator('name')
    def validate_name(cls, v):
        if not v or not str(v).strip():
            raise ValueError('Name cannot be empty')
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', str(v)):
            raise ValueError('Name cannot contain special characters')
        return str(v).strip()

    @field_validator('address')
    def validate_address(cls, v):
        if v is None:
            raise ValueError('Address is required')
        v = str(v).strip()
        if not v:
            raise ValueError('Address cannot be empty')
        return v

    @field_validator('email')
    def validate_oracle_email(cls, v):
        if not v.endswith('@oracle.com'):
            raise ValueError('Email must be an Oracle email address')
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError('Phone number cannot be empty')
        if not isinstance(v, str):
            raise ValueError('Phone number must be a string')
        v = v.strip()
        pattern = r'^\+[0-9]{10}$'  # Exactly 10 digits after +
        if not re.match(pattern, v):
            raise ValueError('Phone number must start with + followed by exactly 10 digits')
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
