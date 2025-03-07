from fastapi import HTTPException, status, Depends, APIRouter

from app import oauth2
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema


router = APIRouter(prefix="/api/v1", tags=["Vote"])


@router.post("/vote", status_code=status.HTTP_202_ACCEPTED)
def vote_post(
    vote: schema.Vote,
    db: Session = Depends(get_db),
    logged_user=Depends(oauth2.get_current_user),
):
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} Does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == logged_user.id
    )

    found_vote = vote_query.first()

    if vote.dir:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {logged_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=logged_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully Added Vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {logged_user.id} has not voted on post {vote.post_id}",
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully Deleted Vote"}
