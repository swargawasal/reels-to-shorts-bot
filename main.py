import os
import asyncio
import logging
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from telegram.error import NetworkError, TimedOut

from downloader import download_video
from uploader import upload_to_youtube

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_HASHTAGS = os.getenv("DEFAULT_HASHTAGS", "#Shorts #YouTubeShorts #Baddie #reels")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

# simple in-memory state: user_id -> {"url": str, "title": str}
user_states = {}

async def safe_reply(update: Update, text: str, parse_mode: str | None = None):
    for _ in range(3):
        try:
            await update.message.reply_text(text, parse_mode=parse_mode)
            return
        except (NetworkError, TimedOut) as e:
            logger.warning(f"Reply failed: {e}. Retrying...")
            await asyncio.sleep(2)
    logger.error("Failed to send message after retries.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, "👋 Send me an Instagram reel link to start.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_id = update.message.from_user.id
    message = update.message.text.strip()

    # Step 1: get IG reel URL
    if "instagram.com/reel/" in message:
        user_states[user_id] = {"url": message}
        preview = "\n".join(DEFAULT_HASHTAGS.split()[:20])
        await safe_reply(
            update,
            f"✅ Got the link!\n\n📌 Using these hashtags:\n{preview}\n\n✏️ Now send the *title* for YouTube Shorts.",
            parse_mode="Markdown",
        )
        return

    # Step 2: get title -> process
    if user_id in user_states and "url" in user_states[user_id] and "title" not in user_states[user_id]:
        user_states[user_id]["title"] = message
        url = user_states[user_id]["url"]
        title = user_states[user_id]["title"]
        hashtags = DEFAULT_HASHTAGS

        await safe_reply(update, "📥 Downloading and uploading...")

        # download (runs blocking code in a worker thread)
        filename = await download_video(url)
        if not filename:
            await safe_reply(update, "❌ Failed to download the video.")
            user_states.pop(user_id, None)
            return

        # upload to YouTube (also in thread)
        yt_link = await upload_to_youtube(filename, hashtags, title)
        if yt_link:
            await safe_reply(update, f"✅ Uploaded to YouTube Shorts!\n🔗 {yt_link}")
        else:
            await safe_reply(update, "❌ Upload failed.")

        user_states.pop(user_id, None)
        return

    # otherwise
    await safe_reply(update, "❓ Please send an Instagram reel link to begin.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception in handler", exc_info=context.error)

def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment.")
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .connect_timeout(5)
        .read_timeout(10)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
