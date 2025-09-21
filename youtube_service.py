from yt_dlp import YoutubeDL

def format_duration(seconds):
    if not seconds and seconds != 0:
        return '-'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        thumbnail_url = info.get("thumbnail")

    result = {
        "title": info["title"],
        "duration": info["duration"],
        "thumbnail": thumbnail_url
    }
    return result

