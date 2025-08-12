import boto3
import sys
import uuid
import os
from datetime import datetime, timezone
from cleaner import clean_csv
from botocore.exceptions import ClientError

# Configurations (can also be set via environment variables)
BUCKET = os.getenv("AWS_S3_BUCKET", "ingestez-jay-20250812")
TABLE = os.getenv("AWS_DYNAMODB_TABLE", "IngestEZUploads")
REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize AWS clients with explicit region
s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE)


def upload_string(name, content):
    key = f"uploads/{name}"
    try:
        s3.put_object(Bucket=BUCKET, Key=key, Body=content.encode("utf-8"))
        return key
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        sys.exit(1)


def add_metadata_to_dynamodb(file_id, filename, s3_key):
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        table.put_item(Item={
            "FileID": file_id,
            "Filename": filename,
            "S3Key": s3_key,
            "UploadedAt": timestamp
        })
    except ClientError as e:
        print(f"Failed to write metadata to DynamoDB: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_clean.py <filename.csv>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isfile(path):
        print(f"File not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_csv(raw)
    filename = f"cleaned-{os.path.basename(path)}"
    file_id = str(uuid.uuid4())

    s3_key = upload_string(filename, cleaned)
    add_metadata_to_dynamodb(file_id, filename, s3_key)

    print(f"Uploaded cleaned file to S3 key: {s3_key}")
    print(f"Metadata added to DynamoDB with FileID: {file_id}")
