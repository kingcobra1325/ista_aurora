import os
from datetime import datetime, timedelta, timezone


class Cursor:
    """
    Stores and manages the last processed 'to' timestamp
    for NewsAPI incremental ingestion.
    """

    def __init__(self, file_path: str = "cursor.txt"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("1970-01-01T00:00:00Z")

    def get_last_to(self) -> datetime:
        with open(self.file_path, "r") as f:
            raw = f.read().strip()

        return datetime.fromisoformat(raw.replace("Z", "")).replace(tzinfo=timezone.utc)

    def get_from(self) -> datetime:
        return self.get_last_to() + timedelta(seconds=1)

    def update_to(self, new_to: datetime):
        # Always store in UTC ISO format
        normalized = new_to.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        with open(self.file_path, "w") as f:
            f.write(normalized)
