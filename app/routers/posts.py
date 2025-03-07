from typing import Optional
from fastapi import APIRouter, Response, HTTPException, status, Depends

from app import oauth2
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from app import schema

router = APIRouter(prefix="/api/v1", tags=["Posts"])


@router.get("/posts", response_model=list[schema.Post])
def posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [schema.Post.model_validate(post) for post in posts]


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(
    post: schema.CreatePost,
    db: Session = Depends(get_db),
    logged_user=Depends(oauth2.get_current_user),
):

    new_post = models.Post(**post.dict(), owner_id=logged_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return schema.Post.model_validate(new_post)


@router.get("/post/{id}", response_model=schema.Post)  # in js it is /post/:id
def post(
    id: int,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return schema.Post.model_validate(post)


@router.put("/post/{id}", response_model=schema.Post)
def update_post(
    id: int,
    post: schema.CreatePost,
    db: Session = Depends(get_db),
    logged_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    postInDB = post_query.first()

    if not postInDB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )

    if postInDB.owner_id != logged_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="recourse access is forbidden",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return schema.Post.model_validate(post_query.first())


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    logged_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )

    if post.owner_id != logged_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="recourse access is forbidden",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
