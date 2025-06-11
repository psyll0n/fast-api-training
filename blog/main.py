from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .hashing import Hash
from .database import schemas, engine, SessionLocal
from passlib.context import CryptContext


# blog/main.py

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


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
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
        "blog": schemas.Blog.model_validate(new_blog),
    }


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_post(id, db: Session = Depends(get_db)):
    """
    Delete a blog post by its ID.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found..."
        )

    db.delete(blog, synchronize_session=False)
    db.commit()
    return {"message": "Blog post deleted successfully"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_post(id, request: schemas.Blog, db: Session = Depends(get_db)) -> dict:
    """
    Update an existing blog post by its ID.
    """
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


@app.get("/blog", status_code=status.HTTP_200_OK, response_model=list[schemas.Blog], tags=["blogs"])
def get_posts(db: Session = Depends(get_db)) -> list[schemas.Blog]:
    """
    Retrieve all blog posts.
    """
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def get_id(id: int, response: Response, db: Session = Depends(get_db)) -> schemas.Blog:
    """
    Retrieve a blog post by its ID.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found..."
        )

    # Convert ORM object to Pydantic schema
    return schemas.ShowBlog.model_validate(blog)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(
    request: schemas.User, db: Session = Depends(get_db)
) -> schemas.ShowUser:
    """
    Create a new user.
    """
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=Hash.bcrrypt(request.password),
    )

    # Check if the username or email already exists
    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.username == request.username)
            | (models.User.email == request.email)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.",
        )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Convert ORM object to Pydantic schema
    return schemas.ShowUser.model_validate(new_user)


@app.get("/user/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)) -> schemas.ShowUser:
    """
    Retrieve a user by their ID.
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    # Check if the user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
        
    # Convert ORM object to Pydantic schema
    return schemas.ShowUser.model_validate(user)
