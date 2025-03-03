# from fastapi.params import Body
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randint

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
    return {"Posts": all_posts}


#  with out validation of Schema Using body from fastapi params
# @app.get("/createPost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"message": "post Created Successfully", "data": payload}


@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    #  automatically validate data will from body will be store in obj post of c;ass Post
    created_post: dict = post.dict()
    created_post["id"] = randint(1, 100000000000000)
    all_posts.append(created_post)
    return {"new_post": created_post}


@app.get("/post/{id}")  # in js it is /post/:id
async def post(id: int, response: Response):
    # id validation is automatically be handle as we have provided type annotation
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return {"post": post}


@app.put("/post/{id}")
async def update_post(id: int, post: Post):
    index = find_post_index(id)
    print(index)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )
    print(post.dict())
    updated_post = post.dict()
    updated_post["id"] = id
    all_posts[index] = updated_post

    return {"data": updated_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    post_index = find_post_index(id)
    if post_index is None:
        # response.status_code = status.HTTP_404_NOT_FOUND no need if your are raising exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} Does not exit",
        )
    all_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
