from yt_dlp import YoutubeDL

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    result = {
        "title": info["title"],
        "duration": info["duration"],
        "thumbnail": info["thumbnail"],
    }
    return result

