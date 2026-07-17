from sqlalchemy import Column, Integer, String
from app.core.database import Base

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    role = Column(String, nullable=False)

    donations = relationship(
    "Donation",
    back_populates="owner"
    )