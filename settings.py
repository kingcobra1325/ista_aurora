import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default: str | None = None):
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        return default
    return value


# News
NEWS_QUERY = get_env("NEWS_QUERY", "technology")
NEWS_API_KEY = get_env("NEWS_API_KEY")

# AWS
AWS_ACCESS_KEY_ID = get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env("AWS_SECRET_ACCESS_KEY")
AWS_REGION = get_env("AWS_REGION", "ap-southeast-2")
AWS_KINESIS_STREAM_NAME = get_env("AWS_KINESIS_STREAM_NAME")

# Redis
REDIS_HOST = get_env("REDIS_HOST", "redis")
REDIS_PORT = get_env("REDIS_PORT", "6379")
