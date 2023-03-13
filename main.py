from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from utils import crud, models, schemas
from utils.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

API_VERSION = "0.1.0"
app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(path="/api")
def api_info():
    return {"version": API_VERSION}


@app.post("/register/users/referrer/{referrer_id}", response_model=schemas.User)
def create_user(referrer_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_referrer = crud.get_user_by_referral_id(db, referral_id=referrer_id)

    if db_referrer and user.referrer_id == referrer_id:
        crud.increase_referrer_points(db, referral_id=referrer_id)
        return crud.create_user(db=db, user=user, referrer_id=referrer_id)
    else:
        raise HTTPException(
            status_code=400, detail="Referrer Not Found. Referral code is invalid")


@app.get("/users/referral_code/{referral_id}", response_model=schemas.User)
def read_user_by_referral_id(referral_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_referral_id(db, referral_id=referral_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/address/{address}", response_model=schemas.User)
def read_user_by_address(address: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_address(db, address=address)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
