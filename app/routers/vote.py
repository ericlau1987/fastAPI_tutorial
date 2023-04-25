# from ..schemas import schemas
import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/votes",
    tags = ['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post {vote.post_id} doesn't exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id
    )
    found_vote = vote_query.first()

    if vote.vote_dir:
        if not found_vote:
            new_vote = models.Vote(user_id=current_user.id, 
                                post_id=vote.post_id)
            db.add(new_vote)
            db.commit()

            return {"message": "successfully added vote"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"The user {current_user.user_id} has voted it already")
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"The vote doesn't exist")
        
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "The vote has been deleted successfully"}
 