import os
import uuid
import logging
import yt_dlp
import asyncio

logger = logging.getLogger("downloader")
logging.getLogger("yt_dlp").setLevel(logging.ERROR)
FFMPEG_BIN = os.environ.get("FFMPEG_BIN", r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin")  # adjust or leave unset
DOWNLOAD_DIR = "downloads"

def _sync_download(url: str) -> str | None:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
        "retries": 3,
        "nocheckcertificate": True,
    }
    # Add Instagram session authentication
    sessionid = os.environ.get("INSTAGRAM_SESSIONID")
    if sessionid:
        ydl_opts["cookiefile"] = None
        ydl_opts["cookies"] = f"sessionid={sessionid}"
    if FFMPEG_BIN and os.path.isdir(FFMPEG_BIN):
        ydl_opts["ffmpeg_location"] = FFMPEG_BIN

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filepath
    except Exception as e:
        logger.error(f"[ERROR] Failed to download: {e}")
        return None

async def download_video(url: str) -> str | None:
    # Make up to 2 attempts (network can hiccup)
    for attempt in range(2):
        path = await asyncio.to_thread(_sync_download, url)
        if path:
            return path
        await asyncio.sleep(2)
    return None




