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


@router.get("/labs", response_model=List[schemas.LabResponse])
def get_labs(db: Session = Depends(get_db)):
    _seed_labs_if_empty(db)
    labs = db.query(models.Lab).all()
    return labs


@router.get("/labs/{id}", response_model=schemas.LabResponse)
def get_lab(id: int, db: Session = Depends(get_db)):
    _seed_labs_if_empty(db)
    lab = db.query(models.Lab).filter(models.Lab.id == id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab
