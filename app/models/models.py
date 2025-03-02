from typing import Optional

from pydantic import BaseModel, EmailStr, PositiveInt, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt = Field(gt=1, lt=130)
    is_subscribed: Optional[bool]  = False