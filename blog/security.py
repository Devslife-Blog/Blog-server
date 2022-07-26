from jose import jwt
from passlib.context import CryptContext

from .settings import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def create_access_token(subject: str):
    to_encode = {"sub": subject}
    encoded_jwt = jwt.encode(to_encode,
                             settings.secret_key,
                             algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
