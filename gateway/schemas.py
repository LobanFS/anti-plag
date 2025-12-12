from pydantic import BaseModel
from typing import List

class SubmitWorkResponse(BaseModel):
    submission_id: str
    file_id: str
    report_id: str
    status: str
    is_plagiarism: bool
    details: str = ""

class ReportItem(BaseModel):
    report_id: str
    submission_id: str
    status: str
    is_plagiarism: bool
    details: str = ""

class WorkReportsResponse(BaseModel):
    work_id: str
    reports: List[ReportItem]
