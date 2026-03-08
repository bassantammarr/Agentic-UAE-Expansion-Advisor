import re


def clean_text(text: str, max_chars: int = 3000) -> str:
    

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\w\s.,AED\-]", "", text)

    text = text.strip()

    return text[:max_chars]