from pydantic import BaseModel

class SubmissionCreate(BaseModel):
    work_id: str
    student_id: str
    student_name: str
    file_id: str

class SubmissionOut(BaseModel):
    id: str
    work_id: str
    student_id: str
    student_name: str
    file_id: str
    submitted_at: str

class ReportOut(BaseModel):
    id: str
    submission_id: str
    status: str
    is_plagiarism: bool
    details: str = ""
    created_at: str
