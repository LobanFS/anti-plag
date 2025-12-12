from sqlalchemy.orm import Session
from db.repositories import SubmissionRepo, ReportRepo
from services.plagiarism_service import check_plagiarism

class AnalysisService:
    def __init__(self, db: Session):
        self.sub_repo = SubmissionRepo(db)
        self.rep_repo = ReportRepo(db)

    def create_submission(self, work_id: str, student_id: str, student_name: str, file_id: str):
        return self.sub_repo.create(work_id, student_id, student_name, file_id)

    async def analyze(self, submission_id: str):
        sub = self.sub_repo.get(submission_id)
        if not sub:
            return None, None

        report = self.rep_repo.create(submission_id=sub.id)

        try:
            subs = self.sub_repo.list_by_work(sub.work_id)
            earlier = [s for s in subs if s.submitted_at < sub.submitted_at]

            # превращаем в dict минимум для plagiarism_service
            current = {"id": sub.id, "work_id": sub.work_id, "student_id": sub.student_id, "file_id": sub.file_id, "submitted_at": sub.submitted_at.isoformat()}
            earlier_d = [{"id": s.id, "student_id": s.student_id, "file_id": s.file_id, "submitted_at": s.submitted_at.isoformat()} for s in earlier]

            is_plag, details = await check_plagiarism(current, earlier_d)
            updated = self.rep_repo.update(report.id, status="COMPLETED", is_plagiarism=is_plag, details=details)
            return sub, updated
        except Exception as e:
            updated = self.rep_repo.update(report.id, status="FAILED", details=str(e))
            return sub, updated

    def reports_by_work(self, work_id: str):
        return self.rep_repo.list_by_work(work_id)
