from typing import List, Optional, Literal
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: UUID


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str


class RoleRead(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class UserAllRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    avatar_url: Optional[str] = None
    role: Optional[RoleRead] = None 

    model_config = {"from_attributes": True}


class UserAdminCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    avatar_url: Optional[str]
    role: str

class UserProfileRead(BaseModel):
    first_name: str
    last_name: str
    email: str

    model_config= {"from_attributes":True}


class CurrentUser(BaseModel):
    id: UUID