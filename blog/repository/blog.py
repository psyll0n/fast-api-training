from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import status, HTTPException


# blog/repository/blog.py


def get_all(db: Session):
    """
    Retrieve all blog posts.
    """
    blogs = db.query(models.Blog).all()

    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # Convert ORM object to Pydantic schema
    return {
        "message": "Blog post created successfully",
        "blog": schemas.Blog.model_validate(new_blog),
        "creator": schemas.ShowUser.model_validate(new_blog.creator),
    }


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog post with id {id} not found",
        )
    db.delete(blog)
    db.commit()
    return {"message": "Blog post deleted successfully"}


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog post with {id} not found...",
        )

    blog.update(request.dict())
    db.commit()

    updated_blog = blog.first()
    return {
        "message": "Blog post updated successfully",
        "blog": schemas.Blog.model_validate(updated_blog),
    }


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found..."
        )

    # Convert ORM object to Pydantic schema
    return schemas.ShowBlog.model_validate(blog)
