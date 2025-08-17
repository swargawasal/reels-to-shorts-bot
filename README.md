# reels-to-shorts-bot
🤖 A Telegram bot that downloads Instagram Reels using a session token from the link you send, and automatically uploads them as YouTube Shorts — fully automated and hands-free.

# Reels to Shorts Bot 🤖

A fully automated Telegram bot that:

1. Downloads Instagram Reels using a session token.
2. Uploads them as YouTube Shorts — hands-free.

## 🔧 Features

- Accepts Instagram Reel links via Telegram.
- Downloads videos using a persistent session token.
- Automatically formats and uploads them to YouTube Shorts.
- Handles token expiration and auth link via Telegram.
- Runs 24/7 with single-browser token authentication.

## ⚙️ Requirements

- Python 3.10+
- Telegram Bot Token
- YouTube API credentials
- Instagram session token

## 🚀 Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/swargawasal/reels-to-shorts-bot.git
   cd reels-to-shorts-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your secrets in a `.env` file:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   YT_CLIENT_ID=your_youtube_client_id
   YT_CLIENT_SECRET=your_youtube_client_secret
   INSTAGRAM_SESSIONID=your_instagram_sessionid
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## 📂 Folder Structure

```
.
├── main.py
├── uploader.py
├── instagram_downloader.py
├── youtube_uploader.py
├── telegram_bot.py
├── .env
├── requirements.txt
└── README.md
```

## 📜 License

This project is licensed under the MIT License.
