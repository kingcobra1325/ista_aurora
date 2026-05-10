import hashlib
from datetime import datetime, timezone


def generate_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def transform(article: dict) -> dict:
    return {
        "article_id": generate_id(article["url"]),
        "source_name": article["source"]["name"],
        "title": article["title"],
        "content": article["content"],
        "url": article["url"],
        "author": article.get("author"),
        "published_at": article["publishedAt"],
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
