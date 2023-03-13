from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    referral_id = Column(String, unique=True, index=True, nullable=False)
    referrer_id = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, unique=True, index=True, nullable=False)
    points = Column(Integer)
