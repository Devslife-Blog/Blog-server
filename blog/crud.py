import datetime
import re
from sqlalchemy.orm import Session

from . import models, schemas, security


def create_user(db: Session, form: schemas.UserCreate):
    new_user = models.User(username=form.username, fullname=form.fullname,
                           email=form.email, password=form.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_fullname(db: Session, fullname: str):
    return db.query(models.User).filter(models.User.fullname == fullname).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


def create_singup_request(db: Session, form: schemas.SignupRequestCreate):
    new_request = models.SignupRequest(username=form.username, fullname=form.fullname,
                                       email=form.email, password=form.password, detail=form.detail, request_at=datetime.datetime.now())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


def get_signup_request(db: Session, id: int):
    return db.query(models.SignupRequest).filter(models.SignupRequest.id == id).first()


def delete_signup_request(db: Session, id: int):
    request = get_signup_request(db, id)
    db.delete(request)
    db.commit()
    return True


def is_email(email):
    return re.fullmatch("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email)
