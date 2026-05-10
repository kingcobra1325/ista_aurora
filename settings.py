import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default: str | None = None):
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        return default
    return value


NEWS_QUERY = get_env("NEWS_QUERY", "technology")
NEWS_API_KEY = get_env("NEWS_API_KEY")
