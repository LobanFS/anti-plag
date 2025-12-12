from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.base import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, index=True)
    work_id = Column(String, index=True, nullable=False)
    student_id = Column(String, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    file_id = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="submission")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)

    status = Column(String, nullable=False, default="PENDING")
    is_plagiarism = Column(Boolean, nullable=False, default=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="reports")
