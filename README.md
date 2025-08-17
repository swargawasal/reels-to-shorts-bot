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
   YT_CLIENT_SECRET=your_client_secret.json
   DEFAULT_HASHTAGS=#shorts etc.. 
   INSTAGRAM_SESSIONID=your_instagram_sessionid
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## 📂 Folder Structure

```
.
├──  requirements.txt
├──  .env
├── downloader.py
├── uploader.py
├── main.py
├── client_secret.json
├── token.pickle
└── README.md
```
⚠️ Troubleshooting

If you face any issues while running the bot, such as authentication errors, upload failures, or session problems, try the following:

Double-check your .env credentials.

Ensure client_secret.json and token.json exist locally and are valid.

For Colab or headless environments, use the token-based authentication method.

If something still doesn’t work, you can use ChatGPT to debug.

## 📜 License

This project is licensed under the MIT License.
