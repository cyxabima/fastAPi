from fastapi import FastAPI, Response, HTTPException, status, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schema


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to this crud Api for social media"}


@app.get("/posts", response_model=list[schema.Post])
async def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return [schema.Post.model_validate(post) for post in posts]


@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return schema.Post.model_validate(new_post)


@app.get("/post/{id}", response_model=schema.Post)  # in js it is /post/:id
async def post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return schema.Post.model_validate(post)


@app.put("/post/{id}", response_model=schema.Post)
async def update_post(id: int, post: schema.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return schema.Post.model_validate(post_query.first())


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
