from urllib.parse import urlparse
from urllib.parse import parse_qs

def validate(text: str):
    url = extract_url(text)
    if url is None:
        return None, "NO_URL"

    parts = urlparse(url)
    host = parts.netloc.lower()
    allowed_hosts = ["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"]
    if host not in allowed_hosts:
        return None, "UNSUPPORTED_HOST"

    path = parts.path
    query = parts.query
    if path != "/watch":
        return None, "NO_VIDEO_ID"
    query = parse_qs(query)
    vid_list = query.get("v")
    if not vid_list:
        return None, "NO_VIDEO_ID"

    video_id = vid_list[0]

    if len(video_id) == 11 and all(ch.isalnum() or ch in "-_" for ch in video_id):
        return video_id, None
    else:
        return None, "NO_VIDEO_ID"


# EXTRACT ONLY LINK
def extract_url(text: str):
    start = text.find("https://")
    if start == -1:
        return None
    end = text.find(" ", start)
    if end == -1:
        candidate = text[start:]
    else:
        candidate = text[start:end]
    return candidate
