from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value will be True
    # if not optional when int is not passed as here it is none it will give error
    # rating: Optional[int] = None


class CreatePost(PostBase):
    # owner_id: str
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostWithVotes___(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class PostWithVotes(Post):
    votes: int

    # class Config:
    #     from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
