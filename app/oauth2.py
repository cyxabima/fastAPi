from datetime import timedelta, timezone, datetime
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import database, models
from . import schema

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/login")


SECRET_KEY = "123Ukasha"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    token_data = schema.TokenData(id=id)
    if token_data is None:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"www.Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    return db.query(models.User).filter(models.User.id == token_data.id).first()
