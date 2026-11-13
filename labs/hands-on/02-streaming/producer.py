"""Send test events to the lab 2 stream.

Usage:
  python3 producer.py STREAM_NAME normal      # 200 well-formed events
  python3 producer.py STREAM_NAME poison      # 1 malformed record, then 50 good ones
  python3 producer.py STREAM_NAME burst       # about 5,000 records/s for 10 s to one shard
"""

import json
import random
import sys
import time

import boto3

kinesis = boto3.client("kinesis")
INSTRUMENTS = ["inst-a", "inst-b", "inst-c"]


def event(i: int) -> dict:
    return {"event_id": f"e{i:06d}", "instrument": random.choice(INSTRUMENTS), "reads": random.randint(0, 900)}


def put(stream: str, payloads: list[bytes]) -> tuple[int, int]:
    """PutRecords in batches of up to 500. Returns (sent, failed)."""
    sent = failed = 0
    for start in range(0, len(payloads), 500):
        chunk = payloads[start : start + 500]
        resp = kinesis.put_records(
            StreamName=stream,
            Records=[{"Data": data, "PartitionKey": str(random.randint(0, 10**6))} for data in chunk],
        )
        sent += len(chunk)
        failed += resp["FailedRecordCount"]
        codes = {r.get("ErrorCode") for r in resp["Records"] if "ErrorCode" in r}
        if codes:
            print("error codes:", codes)
    return sent, failed


def main() -> None:
    stream, mode = sys.argv[1], sys.argv[2]
    if mode == "normal":
        print(put(stream, [json.dumps(event(i)).encode() for i in range(200)]))
    elif mode == "poison":
        payloads = [b"this is not json"] + [json.dumps(event(i)).encode() for i in range(50)]
        print(put(stream, payloads))
    elif mode == "burst":
        total_sent = total_failed = 0
        for second in range(10):
            started = time.time()
            sent, failed = put(stream, [json.dumps(event(i)).encode() for i in range(5000)])
            total_sent += sent
            total_failed += failed
            time.sleep(max(0, 1 - (time.time() - started)))
        print(f"sent={total_sent} failed={total_failed}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
