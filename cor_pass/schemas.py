from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid


class ResponseUser(BaseModel):
    email: EmailStr
    detail: str = "User successfully created"

class LoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class EmailSchema(BaseModel):
    email: EmailStr

class ChangePasswordModel(BaseModel):
    email: EmailStr
    password: str

class UserModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


class TokenData(BaseModel):
    username: Optional[str] = None

class UserDb(BaseModel):
    id: str
    email: EmailStr

    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


class RecordFieldValueModel(BaseModel):
    string_value: Optional[str] = None
    date_value: Optional[datetime] = None
    number_value: Optional[float] = None

class RecordFieldModel(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True

class TagModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RecordModel(BaseModel):
    id: int
    user_id: str
    record_name: str
    website: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    created_at: datetime
    edited_at: datetime
    attachments: Optional[str] = None
    notes: Optional[str] = None
    fields: List[RecordFieldValueModel] = []
    tags: List[TagModel] = []

    class Config:
        from_attributes = True

class CreateRecordModel(BaseModel):
    record_name: str
    website: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    attachments: Optional[str] = None
    notes: Optional[str] = None

class ResponseRecord(BaseModel):
    record: RecordModel
    detail: str = "Record successfully created"

class TagCreateModel(BaseModel):
    name: str

class ResponseTag(BaseModel):
    tag: TagModel
    detail: str = "Tag successfully created"