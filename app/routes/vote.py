from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import models,schema,oauth2,database
from app.database import engine


router = APIRouter(prefix='/vote',tags=['votes'])

@router.post('',status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db : Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post_query:
        vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
        found_vote = vote_query.first()

        if vote.dir ==1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already Voted this post")
            new_vote = models.Votes(post_id=vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message":"vote added","details":new_vote}
            
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Vote doesn't exist for this post by you")
            
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"vote deleted"}
    return {"message":"post does not exist"}
