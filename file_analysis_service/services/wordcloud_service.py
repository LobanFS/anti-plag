import urllib.parse
from clients.file_store_client import download_file

QUICKCHART_URL = "https://quickchart.io/wordcloud"

async def build_wordcloud_url(file_id: str) -> str:
    file_bytes = await download_file(file_id)

    text = file_bytes.decode("utf-8", errors="ignore")

    text = text.replace("\n", " ")

    params = {
        "text": text,
        "format": "png",
        "width": 800,
        "height": 400,
    }

    query = urllib.parse.urlencode(params)
    return f"{QUICKCHART_URL}?{query}"
