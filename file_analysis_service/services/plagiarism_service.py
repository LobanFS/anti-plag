import hashlib
from clients.file_store_client import download_file

def _hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

async def check_plagiarism(current_submission: dict, earlier_submissions: list[dict]) -> tuple[bool, str]:
    cur_bytes = await download_file(current_submission["file_id"])
    cur_hash = _hash(cur_bytes)

    for prev in earlier_submissions:
        if prev["student_id"] == current_submission["student_id"]:
            continue
        prev_bytes = await download_file(prev["file_id"])
        if _hash(prev_bytes) == cur_hash:
            return True, f"Match with submission {prev['id']} by student {prev['student_id']}"
    return False, ""
