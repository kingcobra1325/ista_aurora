import json
from clients.kinesis import get_records
from utils.commons import StringJsonEncoder


def run_query_once(limit=10):
    print("\nFetching records from Kinesis...\n")

    try:
        response = get_records(limit=limit)

        records = response.get("Records", [])

        if not records:
            print("No records found.\n")
            return

        for idx, r in enumerate(records, 1):
            data = json.loads(r["Data"].decode("utf-8"))

            print(f"Record {idx}:")
            print(json.dumps(data, indent=2, cls=StringJsonEncoder))
            print("-" * 40)

        print(f"\nTotal records fetched: {len(records)}\n")

    except Exception as e:
        print(f"[QUERY ERROR] {e}")


if __name__ == "__main__":
    run_query_once()
