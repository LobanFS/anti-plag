import os
import httpx

FILE_STORE_URL = os.getenv("FILE_STORE_URL", "http://file_storing_service:8001")
ANALYSIS_URL = os.getenv("ANALYSIS_URL", "http://file_analysis_service:8002")

_timeout = httpx.Timeout(15.0)

async def upload_file_to_store(filename: str, content: bytes) -> str:
    async with httpx.AsyncClient(timeout=_timeout) as client:
        files = {"file": (filename, content)}
        r = await client.post(f"{FILE_STORE_URL}/files/", files=files)
        r.raise_for_status()
        return r.json()["file_id"]

async def create_submission(work_id: str, student_id: str, student_name: str, file_id: str) -> dict:
    payload = {
        "work_id": work_id,
        "student_id": student_id,
        "student_name": student_name,
        "file_id": file_id,
    }
    async with httpx.AsyncClient(timeout=_timeout) as client:
        r = await client.post(f"{ANALYSIS_URL}/submissions/", json=payload)
        r.raise_for_status()
        return r.json()

async def analyze_submission(submission_id: str) -> dict:
    async with httpx.AsyncClient(timeout=_timeout) as client:
        r = await client.post(f"{ANALYSIS_URL}/submissions/{submission_id}/analyze")
        r.raise_for_status()
        return r.json()

async def get_reports_by_work(work_id: str) -> dict:
    async with httpx.AsyncClient(timeout=_timeout) as client:
        r = await client.get(f"{ANALYSIS_URL}/reports/work/{work_id}")
        r.raise_for_status()
        return r.json()
