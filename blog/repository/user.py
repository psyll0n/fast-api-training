from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from ..hashing import Hash


# blog/repository/user.py


def create(request: schemas.User, db: Session):
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
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


def show(id: int, db: Session) -> schemas.ShowUser:
    user = db.query(models.User).filter(models.User.id == id).first()

    # Check if the user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    # Convert ORM object to Pydantic schema
    return schemas.ShowUser.model_validate(user)