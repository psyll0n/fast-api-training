from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import schemas, engine, SessionLocal


app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Blog, db: Session = Depends(get_db)) -> dict:
    """
    Create a new blog post.
    """
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # Convert ORM object to Pydantic schema
    return {
        "message": "Blog post created successfully",
        "blog": schemas.Blog.from_orm(new_blog)
    }


@app.get("/blog")
def get_posts(db: Session = Depends(get_db)) -> list[schemas.Blog]:
    """
    Retrieve all blog posts.
    """
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def get_id(blog_id: int, response: Response, db: Session = Depends(get_db)) -> schemas.Blog:
    """
    Retrieve a blog post by its ID.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found...")
    return schemas.Blog.from_orm(blog)