from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .database import SessionLocal
from .security import ALGORITHM
from .settings import settings
from . import crud, schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="{}".format(settings.login_url))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not decode token")
    user = crud.get_user(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user
