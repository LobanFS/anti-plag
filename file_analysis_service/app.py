from fastapi import FastAPI

from db.base import Base
from db.session import engine
from api.routes_submissions import router as submissions_router
from api.routes_reports import router as reports_router

app = FastAPI(title="File Analysis Service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(submissions_router, prefix="/submissions")
app.include_router(reports_router, prefix="/reports")
