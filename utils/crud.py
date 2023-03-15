import urllib.parse
from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_referral_id(db: Session, referral_id: str):
    return db.query(models.User).filter(models.User.referral_id == referral_id).first()


def get_user_by_address(db: Session, address: str):
    lowercase_address = address.lower()
    return db.query(models.User).filter(models.User.address == address).first()


def increase_referrer_points(db: Session, referral_id: str):
    db.query(models.User).filter(models.User.referral_id ==
                                 referral_id).update({'points': models.User.points + 10})
    db.commit()
    return


def create_user(db: Session, user: schemas.UserCreate, referrer_id: str):
    lowercase_address = user.address.lower()
    db_user = models.User(referral_id=user.referral_id, referrer_id=referrer_id,
                          email=user.email, address=lowercase_address, points=10)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
