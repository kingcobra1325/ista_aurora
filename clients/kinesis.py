import boto3
import json
import settings
from functools import cache
from utils.commons import StringJsonEncoder


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
    print(
        "Kinesis Ingestion Result\n\n"
        f"{json.dumps(result, indent=2, cls=StringJsonEncoder)}\n\n"
    )


def get_first_shard_id():
    client = get_kinesis_client()

    response = client.describe_stream(StreamName=settings.AWS_KINESIS_STREAM_NAME)

    shards = response["StreamDescription"]["Shards"]

    return shards[0]["ShardId"]


def get_records(limit=10):
    client = get_kinesis_client()

    shard_id = get_first_shard_id()

    iterator_response = client.get_shard_iterator(
        StreamName=settings.AWS_KINESIS_STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON",
    )

    shard_iterator = iterator_response["ShardIterator"]

    records_response = client.get_records(ShardIterator=shard_iterator, Limit=limit)

    return records_response
