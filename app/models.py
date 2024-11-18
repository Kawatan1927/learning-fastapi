from typing import Optional, List

from pydantic import BaseModel
from pydantic.v1 import validator, Field


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    @validator('name')
    def name_must_not_be_empty(self, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v


class Address(BaseModel):
    street: str
    city: str
    zipcode: str = Field(..., regex=r'^\d{5}$')


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = Field(None, regex=r'^\S+@\.\S+$')
    full_name: Optional[str] = None
    address: List[Address] = []

    @validator('username')
    def username_must_not_be_empty(self, v):
        if not v.strip():
            raise ValueError("Username must not be empty")
        return v
