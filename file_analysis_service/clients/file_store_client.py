import os
import httpx

FILE_STORE_URL = os.getenv("FILE_STORE_URL", "http://file_storing_service:8001")
_timeout = httpx.Timeout(15.0)

async def download_file(file_id: str) -> bytes:
    async with httpx.AsyncClient(timeout=_timeout) as client:
        r = await client.get(f"{FILE_STORE_URL}/files/{file_id}")
        r.raise_for_status()
        return r.content
