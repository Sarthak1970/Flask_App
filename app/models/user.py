from pydantic import BaseModel,EmailStr,Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}