import os
import time
import json
import logging
import asyncio
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET_FILE", "client_secret.json")
TOKEN_FILE = os.environ.get("YOUTUBE_TOKEN_FILE", "token.json")

logger = logging.getLogger("uploader")

def _get_service_sync():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # type: ignore[name-defined]
            except Exception:
                creds = None
        if not creds:
            # Desktop/server: open local browser
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(prompt="consent")
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def _upload_sync(file_path: str, hashtags: str, title: str | None) -> str | None:
    service = _get_service_sync()
    final_title = (title or "Guess who?? comment if you got it").strip()

    body = {
        "snippet": {
            "title": final_title,
            "description": hashtags.strip(),
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = service.videos().insert(part="snippet,status", body=body, media_body=media)
    # basic retry loop
    for attempt in range(3):
        try:
            response = request.execute()
            video_id = response.get("id")
            if video_id:
                return f"https://youtube.com/shorts/{video_id}"
            return None
        except HttpError as e:
            logger.warning(f"YouTube API error (attempt {attempt+1}/3): {e}")
            time.sleep(5)
        except Exception as e:
            logger.warning(f"Upload error (attempt {attempt+1}/3): {e}")
            time.sleep(5)
    return None

async def upload_to_youtube(file_path: str, hashtags: str, title: str | None):
    return await asyncio.to_thread(_upload_sync, file_path, hashtags, title)

