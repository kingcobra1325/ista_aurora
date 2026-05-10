from datetime import datetime, timezone, timedelta
import redis
import settings


class RedisCursor:
    def __init__(self, key: str = "news_cursor"):
        self.key = key
        self.r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
        )

    def open_window(self):
        last_to = self.r.get(self.key)

        if last_to is None:
            last_dt = datetime(2026, 4, 10, tzinfo=timezone.utc)
        else:
            last_dt = datetime.fromisoformat(last_to.replace("Z", "")).replace(
                tzinfo=timezone.utc
            )

        current_from = last_dt + timedelta(seconds=1)
        current_to = datetime.now(timezone.utc)

        return current_from, current_to

    def commit(self, new_to: datetime):
        normalized = new_to.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        self.r.set(self.key, normalized)
