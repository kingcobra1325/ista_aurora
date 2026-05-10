import httpx
import settings
import json
from datetime import datetime
from utils.commons import StringJsonEncoder, convert_dt_to_str

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

client = httpx.Client(timeout=10)


def get_news(from_dt: datetime, to_dt: datetime):
    params = {
        "q": settings.NEWS_QUERY,
        "apiKey": settings.NEWS_API_KEY,
        "from": convert_dt_to_str(from_dt),
        "to": convert_dt_to_str(to_dt),
    }
    print(
        "Requesting News Articles from API\n\n"
        f"{json.dumps(params, indent=2, cls=StringJsonEncoder)}\n\n"
    )
    r = client.get(
        NEWS_API_ENDPOINT,
        params=params,
    )
    r.raise_for_status()
    data = r.json()
    print(f"Number of Articles [{len(data["articles"])}]")
    return data
