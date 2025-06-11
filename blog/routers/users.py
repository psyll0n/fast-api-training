
# blog/routers/users.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import database, schemas
from ..repository import user

# blog/routers/users.py

router = APIRouter(
    tags=["users"],
    prefix="/user"  # Adjust the prefix as needed
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/{id}",response_model=schemas.ShowUser,status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(database.get_db)) -> schemas.ShowUser:
    """
    Retrieve a user by their ID.
    """
    return user.show(id, db)


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)) -> schemas.ShowUser:
    """
    Create a new user.
    """
    return user.create(request, db)