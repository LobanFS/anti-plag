from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import httpx

from clients import (
    upload_file_to_store,
    create_submission,
    analyze_submission,
    get_reports_by_work,
)
from schemas import SubmitWorkResponse, WorkReportsResponse

app = FastAPI(title="API Gateway")


@app.post("/works/{work_id}/submissions", response_model=SubmitWorkResponse)
async def submit_work(
    work_id: str,
    file: UploadFile = File(...),
    student_id: str = Form(...),
    student_name: str = Form(...),
):
    try:
        content = await file.read()
        file_id = await upload_file_to_store(file.filename, content)

        submission = await create_submission(work_id, student_id, student_name, file_id)
        report = await analyze_submission(submission["id"])

        return {
            "submission_id": submission["id"],
            "file_id": submission["file_id"],
            "report_id": report["id"],
            "status": report.get("status", "COMPLETED"),
            "is_plagiarism": report.get("is_plagiarism", False),
            "details": report.get("details", ""),
        }

    except httpx.HTTPStatusError as e:
        # если внутренний сервис ответил 4xx/5xx
        raise HTTPException(status_code=502, detail=f"Upstream error: {e.response.status_code} {e.response.text}")
    except httpx.RequestError as e:
        # если внутренний сервис недоступен/таймаут
        raise HTTPException(status_code=503, detail=f"Upstream unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/works/{work_id}/reports", response_model=WorkReportsResponse)
async def reports(work_id: str):
    try:
        data = await get_reports_by_work(work_id)
        reports_list = data.get("reports", [])

        return {
            "work_id": work_id,
            "reports": [
                {
                    "report_id": r["id"],
                    "submission_id": r["submission_id"],
                    "status": r.get("status", "COMPLETED"),
                    "is_plagiarism": r.get("is_plagiarism", False),
                    "details": r.get("details", ""),
                }
                for r in reports_list
            ],
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e.response.status_code} {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Upstream unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
