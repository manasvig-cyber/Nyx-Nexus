from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter()


@router.get("/downloads", response_model=List[schemas.DownloadResponse])
def get_downloads(
    user_id: Optional[int] = Query(default=None, description="Optional player id filter"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Download)
    if user_id is not None:
        query = query.filter(models.Download.user_id == user_id)

    downloads = query.order_by(models.Download.progress.asc(), models.Download.id.asc()).all()

    if not downloads:
        return [
            {
                "id": 1,
                "file_name": "malware_analysis_toolkit.zip",
                "progress": 75,
                "time_remaining": "2 mins",
            }
        ]

    return downloads
