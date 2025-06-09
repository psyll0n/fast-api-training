from pydantic import BaseModel


# In your schemas.py
class Blog(BaseModel):
    title: str
    body: str

    model_config = {
        "from_attributes": True
    }