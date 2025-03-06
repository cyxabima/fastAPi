from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import utils
from .. import schema
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/login")
def login_user(user_credentials: schema.CreateUser, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User Credentials"
        )

    access_token = oauth2.create_access_token(data={"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
