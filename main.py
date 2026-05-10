import time
from datetime import datetime, timezone

from clients.news_api import get_news
from clients.kinesis import ingest
from utils.cursor import Cursor
from utils.processor import transform


def run():
    cursor = Cursor("cursor.txt")

    while True:
        try:
            from_time, to_time = cursor.open_window()

            response = get_news(from_dt=from_time, to_dt=to_time)
            articles = response.get("articles", [])

            if not articles:
                print("No new articles")
                time.sleep(10)
                continue

            batch = []
            latest_time = from_time

            for article in articles:
                record = transform(article)
                batch.append(record)

                published = datetime.fromisoformat(
                    article["publishedAt"].replace("Z", "")
                ).replace(tzinfo=timezone.utc)

                if published > latest_time:
                    latest_time = published

            ingest(batch)

            cursor.commit(latest_time)

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(10)


if __name__ == "__main__":
    run()
