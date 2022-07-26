from sqlalchemy.orm import Session

from . import models, security


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user
