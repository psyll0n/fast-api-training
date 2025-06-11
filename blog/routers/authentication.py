from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, database, token
from ..hashing import Hash


# blog/routers/authentication.py

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"  # Adjust the prefix as needed
)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Authenticate a user with username and password.
    """
    # Check the username and password against your database
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Invalid credentials..."
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=403, detail=f"Invalid credentials for user '{request.username}'"
        )
    # Generate a JWT token or session here and return it...
    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    # If the user is found and the password matches, return a success message
    return {"access_token": access_token, "token_type": "bearer"}