from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from db.models import Submission, Report


class SubmissionRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, work_id: str, student_id: str, student_name: str, file_id: str) -> Submission:
        s = Submission(
            id=str(uuid4()),
            work_id=work_id,
            student_id=student_id,
            student_name=student_name,
            file_id=file_id,
            submitted_at=datetime.utcnow(),
        )
        self.db.add(s)
        self.db.commit()
        self.db.refresh(s)
        return s

    def get(self, submission_id: str) -> Submission | None:
        return self.db.query(Submission).filter(Submission.id == submission_id).first()

    def list_by_work(self, work_id: str) -> list[Submission]:
        return (
            self.db.query(Submission)
            .filter(Submission.work_id == work_id)
            .order_by(Submission.submitted_at.asc())
            .all()
        )


class ReportRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission_id: str, *, status: str = "PENDING", is_plagiarism: bool = False, details: str = "") -> Report:
        r = Report(
            id=str(uuid4()),
            submission_id=submission_id,
            status=status,
            is_plagiarism=is_plagiarism,
            details=details,
            created_at=datetime.utcnow(),
        )
        self.db.add(r)
        self.db.commit()
        self.db.refresh(r)
        return r

    def update(self, report_id: str, *, status: str, is_plagiarism: bool | None = None, details: str | None = None) -> Report | None:
        r = self.db.query(Report).filter(Report.id == report_id).first()
        if not r:
            return None

        r.status = status
        if is_plagiarism is not None:
            r.is_plagiarism = is_plagiarism
        if details is not None:
            r.details = details

        self.db.commit()
        self.db.refresh(r)
        return r

    def list_by_work(self, work_id: str) -> list[Report]:
        submissions = (
            self.db.query(Submission)
            .filter(Submission.work_id == work_id)
            .all()
        )
        submission_ids = [s.id for s in submissions]

        if not submission_ids:
            return []

        return (
            self.db.query(Report)
            .filter(Report.submission_id.in_(submission_ids))
            .order_by(Report.created_at.asc())
            .all()
        )
