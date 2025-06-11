from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .hashing import Hash
from .database import schemas, engine, get_db
from passlib.context import CryptContext
from .routers import authentication, blog, users

# blog/main.py

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(users.router)

