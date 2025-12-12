from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "data"
FILES_DIR.mkdir(exist_ok=True)


@router.post("/", summary="Загрузить файл")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    file_id = str(uuid4())
    ext = Path(file.filename).suffix
    saved_path = FILES_DIR / f"{file_id}{ext}"

    content = await file.read()
    saved_path.write_bytes(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(content),
    }


@router.get("/{file_id}", summary="Скачать файл по id")
async def download_file(file_id: str):
    candidates = list(FILES_DIR.glob(f"{file_id}*"))
    if not candidates:
        raise HTTPException(status_code=404, detail="File not found")
    path = candidates[0]
    return FileResponse(path, filename=path.name)
