from fastapi import FastAPI
from routes import router as files_router

app = FastAPI(title="File Storing Service")

app.include_router(files_router, prefix="/files")
