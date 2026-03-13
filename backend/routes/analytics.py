from datetime import date, datetime, time, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter()


SUCCESS_RESULTS = ["success", "passed", "complete", "completed"]
DEFAULT_PERFORMANCE = {
    "missions_completed": 42,
    "success_rate": 87,
    "weekly_activity": [10, 15, 20, 18, 25, 30],
}
DEFAULT_XP_TRENDS = {
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "values": [120, 200, 180, 260, 300, 400, 350],
}
SERIES_DAYS = 7


def _resolve_user_scope(user_id: Optional[int], db: Session) -> Optional[int]:
    if user_id is not None:
        return user_id

    first_user = db.query(models.User.id).order_by(models.User.id.asc()).first()
    return first_user[0] if first_user else None


def _build_daily_sum_series(db: Session, column, user_id: Optional[int]) -> tuple[List[str], List[int]]:
    today = date.today()
    labels: List[str] = []
    values: List[int] = []

    for offset in range(SERIES_DAYS - 1, -1, -1):
        current_day = today - timedelta(days=offset)
        start_dt = datetime.combine(current_day, time.min)
        end_dt = start_dt + timedelta(days=1)

        query = db.query(func.coalesce(func.sum(column), 0)).filter(
            models.Analytics.timestamp >= start_dt,
            models.Analytics.timestamp < end_dt,
        )
        if user_id is not None:
            query = query.filter(models.Analytics.user_id == user_id)

        labels.append(current_day.strftime("%a"))
        values.append(int(query.scalar() or 0))

    return labels, values


@router.get("/performance", response_model=schemas.PerformanceResponse)
def get_performance(
    user_id: Optional[int] = Query(default=None, description="Optional player id filter"),
    db: Session = Depends(get_db),
):
    scoped_user_id = _resolve_user_scope(user_id, db)

    attempts_query = db.query(models.Attempt)
    analytics_query = db.query(models.Analytics)
    if scoped_user_id is not None:
        attempts_query = attempts_query.filter(models.Attempt.user_id == scoped_user_id)
        analytics_query = analytics_query.filter(models.Analytics.user_id == scoped_user_id)

    missions_completed = int(
        analytics_query.with_entities(
            func.coalesce(func.sum(models.Analytics.missions_completed), 0)
        ).scalar()
        or 0
    )

    total_attempts = attempts_query.count()
    successful_attempts = attempts_query.filter(
        func.lower(models.Attempt.attempt_result).in_(SUCCESS_RESULTS)
    ).count()

    _, weekly_activity = _build_daily_sum_series(
        db,
        models.Analytics.missions_completed,
        scoped_user_id,
    )

    if sum(weekly_activity) == 0 and total_attempts > 0:
        weekly_activity = []
        today = date.today()
        for offset in range(SERIES_DAYS - 1, -1, -1):
            current_day = today - timedelta(days=offset)
            start_dt = datetime.combine(current_day, time.min)
            end_dt = start_dt + timedelta(days=1)
            day_attempts_query = db.query(func.count(models.Attempt.id)).filter(
                models.Attempt.timestamp >= start_dt,
                models.Attempt.timestamp < end_dt,
            )
            if scoped_user_id is not None:
                day_attempts_query = day_attempts_query.filter(
                    models.Attempt.user_id == scoped_user_id
                )
            weekly_activity.append(int(day_attempts_query.scalar() or 0))

    if missions_completed == 0 and total_attempts == 0 and sum(weekly_activity) == 0:
        return DEFAULT_PERFORMANCE

    success_rate = int(round((successful_attempts / total_attempts) * 100)) if total_attempts else 0

    return {
        "missions_completed": missions_completed,
        "success_rate": success_rate,
        "weekly_activity": weekly_activity,
    }


@router.get("/xp-trends", response_model=schemas.XPTrendResponse)
def get_xp_trends(
    user_id: Optional[int] = Query(default=None, description="Optional player id filter"),
    db: Session = Depends(get_db),
):
    scoped_user_id = _resolve_user_scope(user_id, db)
    labels, values = _build_daily_sum_series(db, models.Analytics.xp_gained, scoped_user_id)

    if sum(values) == 0:
        return DEFAULT_XP_TRENDS

    return {
        "labels": labels,
        "values": values,
    }


@router.get("/analytics/user-progress", response_model=schemas.UserProgressResponse)
def get_user_progress(
    user_id: Optional[int] = Query(default=None, description="Optional player id filter"),
    db: Session = Depends(get_db),
):
    scoped_user_id = _resolve_user_scope(user_id, db)
    if scoped_user_id is None:
        return {"labs_completed": 0, "ctf_completed": 0, "xp": 0}

    user = db.query(models.User).filter(models.User.id == scoped_user_id).first()
    
    # Count labs completed (excluding CTFs)
    labs_completed = db.query(models.Attempt).filter(
        models.Attempt.user_id == scoped_user_id,
        models.Attempt.attempt_result == "completed"
    ).join(models.Lab).filter(~models.Lab.title.contains("ctf")).count()

    # Count CTFs completed
    ctf_completed = db.query(models.Attempt).filter(
        models.Attempt.user_id == scoped_user_id,
        models.Attempt.attempt_result == "completed"
    ).join(models.Lab).filter(models.Lab.title.contains("ctf")).count()

    return {
        "labs_completed": labs_completed,
        "ctf_completed": ctf_completed,
        "xp": user.xp if user else 0
    }
