from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    organization_name: str
    contact_person: str
    email: EmailStr
    password: str
    contact_number: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str