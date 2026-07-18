from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

from sqlalchemy.orm import relationship
class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    expiry_time = Column(DateTime, nullable=False)
    pickup_address = Column(String, nullable=False)
    status = Column(String, default="Available")

    owner_id = Column(Integer, ForeignKey("users.id"))

    claimed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    owner = relationship(
        "User",
        back_populates="donations",
        foreign_keys=[owner_id]
    )

    claimer = relationship(
        "User",
        foreign_keys=[claimed_by]
    )