from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

#PATHES FOR
DOWNLOAD_DIR_AUDIO = Path('C:/Users/999fps/Desktop/tg_bot_downloads/AUDIO')
DOWNLOAD_DIR_VIDEO = Path('C:/Users/999fps/Desktop/tg_bot_downloads/VIDEO')