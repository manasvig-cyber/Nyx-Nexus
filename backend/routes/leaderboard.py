from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter()


DEFAULT_LEADERBOARD = [
    {"id": 1, "user_id": 1, "username": "Neo", "xp": 15000, "rank_position": 1},
    {"id": 2, "user_id": 2, "username": "Trinity", "xp": 14200, "rank_position": 2},
    {"id": 3, "user_id": 3, "username": "Morpheus", "xp": 13900, "rank_position": 3},
]


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    records = (
        db.query(models.Leaderboard, models.User)
        .join(models.User, models.User.id == models.Leaderboard.user_id)
        .order_by(models.Leaderboard.rank_position.asc(), models.Leaderboard.xp.desc())
        .all()
    )

    if not records:
        users = (
            db.query(models.User)
            .order_by(models.User.xp.desc(), models.User.created_at.asc())
            .limit(50)
            .all()
        )

        if not users:
            return DEFAULT_LEADERBOARD

        return [
            {
                "id": index,
                "user_id": user.id,
                "username": user.username,
                "xp": user.xp,
                "rank_position": index,
            }
            for index, user in enumerate(users, start=1)
        ]

    leaderboard_payload = []
    has_updates = False
    for index, (entry, user) in enumerate(records, start=1):
        if entry.rank_position != index or entry.xp != user.xp:
            entry.rank_position = index
            entry.xp = user.xp
            has_updates = True

        leaderboard_payload.append(
            {
                "id": entry.id,
                "user_id": entry.user_id,
                "username": user.username,
                "xp": entry.xp,
                "rank_position": entry.rank_position,
            }
        )

    if has_updates:
        db.commit()

    return leaderboard_payload
