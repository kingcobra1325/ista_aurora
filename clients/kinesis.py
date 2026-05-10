import boto3
import json
import settings
from functools import cache


@cache
def get_kinesis_client():
    return boto3.client("kinesis", region_name=settings.AWS_REGION)


def ingest(records):
    client = get_kinesis_client()
    result = client.put_records(
        StreamName=settings.AWS_KINESIS_STREAM_NAME,
        Records=[
            {
                "Data": json.dumps(r).encode("utf-8"),
                "PartitionKey": r["source_name"],
            }
            for r in records
        ],
    )
    print(f"Kinesis Ingestion Result\n\n{json.dumps(result, indent=2)}\n\n")
