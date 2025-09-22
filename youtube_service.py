from yt_dlp import YoutubeDL
from config import DOWNLOAD_DIR_VIDEO, DOWNLOAD_DIR_AUDIO


def format_duration(seconds):
    if not seconds and seconds != 0:
        return '-'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f'{h} час {m} минут {s} секунд'
    elif h == 0 and m > 0:
        return f'{m} минут {s} секунд'
    elif h == 0 and m == 0:
        return f'{s} секунд'

def human_size(size_bytes):
    if not size_bytes:
        return "—"
    gb = size_bytes // (1024 ** 3)
    mb = (size_bytes % (1024 ** 3)) // (1024 ** 2)
    if gb > 0:
        return f"{gb} GB {mb} MB"
    else:
        return f"{mb} MB"

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        thumbnail_url = info.get("thumbnail")
        formats = info.get("formats", [])

        size_720 = None
        size_1080 = None
        size_audio = None

        for f in formats:
            if f.get("height") == 720 and f.get("ext") == "webm":
                size_720 = f.get("filesize") or f.get("filesize_approx")
            elif f.get("height") == 1080 and f.get("ext") == "mp4":
                size_1080 = f.get("filesize") or f.get("filesize_approx")
            elif f.get("vcodec") == "none":
                size_audio = f.get("filesize") or f.get("filesize_approx")

    result = {
        "title": info["title"],
        "duration": info["duration"],
        "thumbnail": thumbnail_url,
        "size_720": size_720,
        "size_1080": size_1080,
        "size_audio": size_audio,
        "size_720_text": human_size(size_720),
        "size_1080_text": human_size(size_1080),
        "size_audio_text": human_size(size_audio),
    }
    return result

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": str(DOWNLOAD_DIR_AUDIO / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info).replace(".webm", ".mp3")

def download_video(video_id, height):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "format": "",
        "merge_output_format": "mp4",
        "outtmpl": str(DOWNLOAD_DIR_VIDEO / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "no_warnings": True,
    }
    if height == 720:
        ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best"
    elif height == 1080:
        ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best"
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)