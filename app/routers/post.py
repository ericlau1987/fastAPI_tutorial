# from ..schemas import schemas
import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):


    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                        #  isouter=True).group_by(models.Post.id).all()

    # more efficient
    votes_count_query = db.query(models.Vote.post_id, func.count(models.Vote.user_id).label("votes")).group_by(models.Vote.post_id).subquery()
    results = db.query(models.Post, func.coalesce(votes_count_query.c.votes, 0).label("votes")).join(votes_count_query, votes_count_query.c.post_id==models.Post.id,
                                               isouter=True).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    return results


@router.get("/current_users_posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10):

    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)): # add int to convert str to integer

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post or post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorised to perform request action")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform request action")

    else: 
        post.delete(synchronize_session=False)
        db.commit()
    # when deleting data, we dont want to return any data 
    # instead, we just send the status back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform request action")
    else:
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()

    return post_query.first()