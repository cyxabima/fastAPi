from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value will be True
    # if not optional when int is not passed as here it is none it will give error
    # rating: Optional[int] = None


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
