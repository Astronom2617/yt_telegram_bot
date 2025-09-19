from urllib.parse import urlparse

def validate(text: str):
    url = extract_url(text)
    if url is None:
        return None, "NO_URL"

    parts = urlparse(url)
    host = parts.netloc.lower()
    allowed_hosts = ["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"]
    if host not in allowed_hosts:
        return None, "UNSUPPORTED_HOST"
    return url, None


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
