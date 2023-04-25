from fastapi import FastAPI
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import models
 
from database import engine, SessionLocal, get_db
from routers import post, user, property, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(property.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}