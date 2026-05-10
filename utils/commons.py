import json
from datetime import datetime, date, timezone


class StringJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat() + "Z"

        if isinstance(obj, date):
            return obj.isoformat()

        return str(obj)


def convert_dt_to_str(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
