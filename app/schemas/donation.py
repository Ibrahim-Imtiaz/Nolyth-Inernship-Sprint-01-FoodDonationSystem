from datetime import datetime
from pydantic import BaseModel


class DonationCreate(BaseModel):
    food_name: str
    quantity: int
    expiry_time: datetime
    pickup_address: str


class DonationResponse(BaseModel):
    id: int
    food_name: str
    quantity: int
    expiry_time: datetime
    pickup_address: str
    status: str
    owner_id: int

    class Config:
        from_attributes = True

class DonationUpdate(BaseModel):
    food_name: str
    quantity: int
    expiry_time: datetime
    pickup_address: str