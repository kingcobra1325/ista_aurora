from pydantic import BaseModel, Field
from datetime import datetime


class NewsArticle(BaseModel):
    article_id: str
    source_name: str
    title: str
    content: str
    url: str
    author: str | None = None
    published_at: datetime
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
