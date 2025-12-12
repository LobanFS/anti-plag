from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import SessionLocal
from services.analysis_service import AnalysisService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/work/{work_id}")
def reports_by_work(work_id: str, db: Session = Depends(get_db)):
    service = AnalysisService(db)
    reports = service.reports_by_work(work_id)
    return {
        "work_id": work_id,
        "reports": [
            {
                "id": r.id,
                "submission_id": r.submission_id,
                "status": r.status,
                "is_plagiarism": r.is_plagiarism,
                "details": r.details or "",
                "created_at": r.created_at.isoformat(),
            }
            for r in reports
        ],
    }
