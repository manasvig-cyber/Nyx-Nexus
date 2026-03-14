from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter()


DEFAULT_LABS = [
    {
        "title": "SQL Injection Lab",
        "difficulty": "Medium",
        "status": "active",
        "icon": "database",
    },
    {
        "title": "XSS Forensics Arena",
        "difficulty": "Hard",
        "status": "active",
        "icon": "terminal",
    },
    {
        "title": "Packet Tracer Ops",
        "difficulty": "Easy",
        "status": "queued",
        "icon": "network",
    },
]


def _seed_labs_if_empty(db: Session) -> None:
    if db.query(models.Lab.id).first():
        return

    db.add_all([models.Lab(**lab) for lab in DEFAULT_LABS])
    db.commit()

@router.get("/labs")
def get_labs(user_id: int, db: Session = Depends(get_db)):

    _seed_labs_if_empty(db)

    labs = db.query(models.Lab).all()

    results = []

    for lab in labs:

        completed = db.query(models.Attempt).filter(
            models.Attempt.user_id == user_id,
            models.Attempt.lab_id == lab.id,
            models.Attempt.attempt_result == "completed"
        ).first()

        results.append({
            "id": lab.id,
            "name": lab.title,
            "difficulty": lab.difficulty,
            "completed": completed is not None
        })

    return results



@router.get("/labs")
def get_labs(user_id: int, db: Session = Depends(get_db)):

    _seed_labs_if_empty(db)

    labs = db.query(models.Lab).all()

    results = []

    for lab in labs:

        completed = db.query(models.Attempt).filter(
            models.Attempt.user_id == user_id,
            models.Attempt.lab_id == lab.id,
            models.Attempt.attempt_result == "completed"
        ).first()

        results.append({
            "id": lab.id,
            "name": lab.title,
            "difficulty": lab.difficulty,
            "completed": completed is not None
        })

    return results



@router.post("/labs/complete")
def complete_lab(payload: schemas.LabCompletionRequest, db: Session = Depends(get_db)):
    # 1. Update user XP
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        # For demo purposes, if user 1 doesn't exist, we might want to create it or just error
        # But let's assume user exists or use a default one if needed.
        # However, it's better to raise 404.
        raise HTTPException(status_code=404, detail="User not found")

    # Determine XP based on lab/CTF
    xp_to_add = 100 # Default
    if "ctf" in payload.lab_id.lower():
        xp_to_add = 150
    elif "network" in payload.lab_id.lower():
        xp_to_add = 200
    
    user.xp += xp_to_add
    
    # Update rank based on XP (simple logic)
    if user.xp > 1000:
        user.rank = "Specialist"
    if user.xp > 2000:
        user.rank = "Expert"

    # 2. Find or create the lab in the database
    lab = db.query(models.Lab).filter(models.Lab.title == payload.lab_id).first()
    if not lab:
        lab = models.Lab(title=payload.lab_id, difficulty="Medium", status="active")
        db.add(lab)
        db.flush()

    # 3. Record the attempt (completion)
    attempt = models.Attempt(
        user_id=user.id,
        lab_id=lab.id,
        attempt_result="completed",
        timestamp=datetime.utcnow()
    )
    db.add(attempt)

    # 4. Update Analytics
    analytics_event = models.Analytics(
        user_id=user.id,
        xp_gained=xp_to_add,
        missions_completed=1,
        timestamp=datetime.utcnow()
    )
    db.add(analytics_event)

    # 5. Update Leaderboard
    leaderboard = db.query(models.Leaderboard).filter(models.Leaderboard.user_id == user.id).first()
    if leaderboard:
        leaderboard.xp = user.xp
    else:
        db.add(models.Leaderboard(user_id=user.id, xp=user.xp, rank_position=0))

    db.commit()
    return {"status": "success", "xp_gained": xp_to_add, "new_total_xp": user.xp}
