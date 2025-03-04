# from fastapi.params import Body
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# import psycopg
from connectDB import db_connect

app = FastAPI()
all_posts: list[dict] = [
    {
        "title": "Hello world",
        "content": "My first Web Api",
        "published": True,
        "rating": None,
        "id": 1,
    },
    {
        "title": "Cpp",
        "content": "C++ is an amazing language",
        "published": True,
        "rating": None,
        "id": 2,
    },
]

conn, cursor = db_connect()


def find_post(id):
    for post in all_posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for index, post in enumerate(all_posts):
        if post["id"] == id:
            return index


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value will be True
    # if not optional when int is not passed as here it is none it will give error
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to this crud Api for social media"}


@app.get("/posts")
async def posts():
    cursor.execute("SELECT * FROM posts")
    all_posts = cursor.fetchall()
    return {"Posts": all_posts}


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/post/{id}")  # in js it is /post/:id
async def post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return {"post": post}


@app.put("/post/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )

    return {"data": updated_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
