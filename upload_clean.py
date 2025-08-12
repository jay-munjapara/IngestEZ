import boto3
import sys
from cleaner import clean_csv

BUCKET = "ingestez-jay-20250812"  # Replace with your bucket name

s3 = boto3.client("s3")


def upload_string(name, content):
    key = f"uploads/{name}"
    s3.put_object(Bucket=BUCKET, Key=key, Body=content.encode("utf-8"))
    return key


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_clean.py <filename.csv>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_csv(raw)
    filename = f"cleaned-{path.split('/')[-1]}"
    key = upload_string(filename, cleaned)
    print(f"Uploaded cleaned file to S3 key: {key}")
