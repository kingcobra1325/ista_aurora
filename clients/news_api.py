import httpx
import settings
import json

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

client = httpx.Client(timeout=10)


def get_news(to_dt: str, from_dt: str = None):
    params = {
        "q": settings.NEWS_QUERY,
        "apiKey": settings.NEWS_API_KEY,
        "to": to_dt,
        "sortBy": "publishedAt",
    }
    if from_dt:
        params["from"] = from_dt
    print(f"Requesting News Articles from API\n\n{json.dumps(params, indent=2)}\n\n")
    r = client.get(
        NEWS_API_ENDPOINT,
        params=params,
    )
    r.raise_for_status()
    return r.json()
