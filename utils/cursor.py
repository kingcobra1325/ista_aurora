import os
from datetime import datetime, timedelta, timezone


class Cursor:
    def __init__(self, file_path: str = "cursor.txt"):
        self.file_path = file_path
        self._ensure_file()

        self._current_from = None
        self._current_to = None

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("2026-04-10T00:00:00Z")

    def _read_last_to(self) -> datetime:
        with open(self.file_path, "r") as f:
            raw = f.read().strip()

        return datetime.fromisoformat(raw.replace("Z", "")).replace(tzinfo=timezone.utc)

    def open_window(self):
        self._current_from = self._read_last_to() + timedelta(seconds=1)
        self._current_to = datetime.now(timezone.utc)

        return self._current_from, self._current_to

    def commit(self, new_to: datetime):
        normalized = new_to.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        with open(self.file_path, "w") as f:
            f.write(normalized)

        self._current_from = None
        self._current_to = None

    # optional: debug
    def current_window(self):
        return self._current_from, self._current_to
