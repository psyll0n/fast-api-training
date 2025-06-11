from fastapi import APIRouter, Depends, status
from ..import schemas, database
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog


# blog/routers/blog.py

router = APIRouter(
    tags=["blogs"],
    prefix="/blog"  # Adjust the prefix as needed
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Blog])
def get_posts(db: Session = Depends(database.get_db)) -> list[schemas.Blog]:
    """
    Retrieve all blog posts.
    """
    return blog.get_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_id(id: int, db: Session = Depends(database.get_db)) -> schemas.Blog:
    """
    Retrieve a blog post by its ID.
    """
    return blog.show(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Blog, db: Session = Depends(database.get_db)) -> dict:
    """
    Create a new blog post.
    """
    return blog.create(request, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id, request: schemas.Blog, db: Session = Depends(database.get_db)) -> dict:
    """
    Update an existing blog post by its ID.
    """
    return blog.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(database.get_db)):
    """
    Delete a blog post by its ID.
    """
    return blog.destroy(id, db)