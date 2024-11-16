from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import validator


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


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

    @validator('username')
    def username_must_not_be_empty(self, v):
        if not v.strip():
            raise ValueError("Username must not be empty")
        return v
