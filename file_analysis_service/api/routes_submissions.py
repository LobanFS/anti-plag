from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.wordcloud_service import build_wordcloud_url
from db.session import SessionLocal
from services.analysis_service import AnalysisService
from schemas import SubmissionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", summary="Создать сдачу (submission)")
def create_submission(payload: SubmissionCreate, db: Session = Depends(get_db)):
    service = AnalysisService(db)
    s = service.create_submission(
        work_id=payload.work_id,
        student_id=payload.student_id,
        student_name=payload.student_name,
        file_id=payload.file_id,
    )
    return {
        "id": s.id,
        "work_id": s.work_id,
        "student_id": s.student_id,
        "student_name": s.student_name,
        "file_id": s.file_id,
        "submitted_at": s.submitted_at.isoformat(),
    }

@router.post("/{submission_id}/analyze", summary="Запустить анализ и получить отчет")
async def analyze_submission(submission_id: str, db: Session = Depends(get_db)):
    service = AnalysisService(db)
    sub, rep = await service.analyze(submission_id)

    if not sub or not rep:
        raise HTTPException(status_code=404, detail="Submission not found")

    return {
        "id": rep.id,
        "submission_id": rep.submission_id,
        "status": rep.status,
        "is_plagiarism": rep.is_plagiarism,
        "details": rep.details or "",
        "created_at": rep.created_at.isoformat(),
    }

@router.get("/{submission_id}/wordcloud", summary="Облако слов для работы")
async def submission_wordcloud(submission_id: str, db: Session = Depends(get_db)):
    service = AnalysisService(db)
    sub = service.sub_repo.get(submission_id)

    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    url = await build_wordcloud_url(sub.file_id)

    return {
        "submission_id": submission_id,
        "wordcloud_url": url,
    }
