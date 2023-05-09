from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags = ['Users'] # this is to show a group in property
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    new_user_email = user.email
    # check whether the email exists in database
    user = db.query(models.User).filter(models.User.email == new_user_email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"{new_user_email} exists. Please log in or click forget password."
                            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, response: Response, db: Session = Depends(get_db)): # add int to convert str to integer

    # hash the password 
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user or user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} was not found")

    return user 