# 🎬 YouTube Downloader Bot  

**_A Telegram bot for downloading YouTube videos and audio.  
Supports quality selection, shows preview, duration, and approximate file size._**  

---

## 🚀 Features  
- 📹 Download videos in **720p** and **1080p**  
- 🎧 Convert audio to **MP3**  
- 🖼 Display video preview and title  
- ⏱ Show video duration in human-readable format  
- 📦 Estimate file sizes before downloading  

---

## 🛠 Tech Stack  
- [Python 3.11+](https://www.python.org/)  
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API framework  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — media downloading and parsing  
- [FFmpeg](https://ffmpeg.org/) — media processing  

---

## 📂 Project Structure  
yt_telegram_bot/

│── app/

│ ├── handlers.py _# command handlers_

│ ├── keyboards.py _# inline & reply keyboards_

│ ├── state.py _# bot states_

│── youtube_service.py _# downloading & video info logic_

│── validators.py _# URL validation_

│── config.py _# configuration_

│── bot.py _# entry point_

│── requirements.txt _# dependencies_

│── README.md _# documentation_

---
## ⚡ Installation & Usage
1. **Clone the repository:** 
   ```bash
   git clone https://github.com/your-username/yt_telegram_bot.git
   cd yt_telegram_bot
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Install FFmpeg**
4. **Create a .env file with your bot token:**
   ```bash
   BOT_TOKEN=your_token_here
5. **Run the bot:**
   ```bash
   python bot.py

---
## 🎯 Example Output
📹 **Found a video!**

🎬 **Title:** the FUN way to learn programming

⏳ **Duration:** 12 minutes 07 seconds

📦 **File sizes (approx.):**
- 720p: ~32 MB
- 1080p: ~43 MB
- MP3 (audio): ~10 MB

---
## 📌 TODO / Roadmap
- _Add playlist support_
- _Implement download progress bar_
- _Deploy bot to run 24/7 on a server_
- _Improve logging system_

---
## Author
**Astro2617 🚀**
