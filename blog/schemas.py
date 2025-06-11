from typing import List
from pydantic import BaseModel


# blog/schemas.py
class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    model_config = {"from_attributes": True}


class User(BaseModel):
    username: str
    email: str
    password: str

    model_config = {"from_attributes": True}


class ShowUser(BaseModel):
    username: str
    email: str
    # This will hold a list of Blog objects associated with the user
    blogs: list[Blog] = []

    model_config = {"from_attributes": True}


class ShowBlog(Blog):
    title: str
    body: str
    creator: ShowUser
    model_config = {"from_attributes": True}
