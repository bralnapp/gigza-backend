from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    address: str
    referral_id: str
    referrer_id: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    points: int

    class Config:
        orm_mode = True
