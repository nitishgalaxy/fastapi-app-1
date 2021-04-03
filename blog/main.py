from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas
import models 
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session 
from typing import List 
from hashing import Hash
from routers import blog, user, authentication


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
