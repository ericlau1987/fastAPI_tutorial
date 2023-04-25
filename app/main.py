from fastapi import FastAPI
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from random import randrange
import models
 
from database import engine, SessionLocal, get_db
from routers import post, user, property, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(property.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}