import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


# FastAPI application to demonstrate basic routing and query parameters.
# This code snippet creates a simple FastAPI application with several endpoints
# that handle different routes and query parameters.
# It includes an index route, a route for unpublished blogs, a route to get a blog by ID,
# and a route to get comments for a specific blog by ID.


app = FastAPI()


@app.get("/")
def index(limit: int=10, published: bool=True, sort: Optional[str]=None) -> dict:
    if published:
        return {"data": f"{limit} published blog(s) from the db"}
    return {"data": f"{limit} blog(s) from the db"}


@app.get("/blog/unpublished")
def unpublished_blogs() -> dict:
    # Fetch unpublished blogs
    return {"data": "unpublished blogs"}


@app.get("/blog/{id}")
def get_ids(id: int) -> dict:
    # Fetch blog by id
    return {"data": id}


@app.get("/blog/{id}/comments")
def get_comments(id: int) -> dict:
    # Fetch comments for the blog by id
    return {"data": f"Comments for blog {id}"}


# Define a Pydantic model for the blog ID
# Pydantic model for blog data
class Blog(BaseModel):
    title: str
    content: str
    published: bool = True


@app.post("/blog")
def create_blog(request: Blog) -> dict:
    # Create a new blog
    return {"data": f"Blog created with title as: {request.title}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)