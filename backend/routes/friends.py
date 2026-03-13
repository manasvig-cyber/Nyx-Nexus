from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter()


@router.get("/friends", response_model=List[schemas.FriendResponse])
def get_friends(
    user_id: Optional[int] = Query(default=None, description="Optional player id filter"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Friend)
    if user_id is not None:
        query = query.filter(models.Friend.user_id == user_id)

    friends = query.order_by(
        case((models.Friend.status == "online", 0), else_=1),
        models.Friend.last_seen.desc(),
    ).all()

    if not friends:
        return [
            {"username": "CyberAlex", "status": "online"},
            {"username": "HexHunter", "status": "offline"},
        ]

    return [{"username": f.friend_username, "status": f.status} for f in friends]
