from fastapi import HTTPException, status, Depends, APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema, utils

router = APIRouter(prefix="/api/v1", tags=["Users"])


@router.post("/user", response_model=schema.UserOut)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schema.UserOut.model_validate(new_user)


@router.get("/user/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} Doesn't exits",
        )

    return schema.UserOut.model_validate(user)
