from pydantic import BaseModel


# In your schemas.py
class Blog(BaseModel):
    title: str
    body: str

    model_config = {"from_attributes": True}


class ShowBlog(Blog):
    class Config:
        orm_mode = True
        # This allows the model to work with ORM objects
        # and convert them to Pydantic models.


class User(BaseModel):
    username: str
    email: str
    password: str

    model_config = {"from_attributes": True}


class ShowUser(BaseModel):
    username: str
    email: str

    model_config = {"from_attributes": True}
