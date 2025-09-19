def validate(text: str):
    if "http" in text:
        return text, None
    else:
        return None, "NO_URL"


