import boto3
import json
import uuid
from datetime import datetime, timezone
from cleaner import clean_csv

BUCKET = "ingestez-jay-20250812"
TABLE = "IngestEZUploads"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE)


def upload_string(name, content):
    key = f"uploads/{name}"
    s3.put_object(Bucket=BUCKET, Key=key, Body=content.encode("utf-8"))
    return key


def add_metadata_to_dynamodb(file_id, filename, s3_key):
    timestamp = datetime.now(timezone.utc).isoformat()
    table.put_item(Item={
        "FileID": file_id,
        "Filename": filename,
        "S3Key": s3_key,
        "UploadedAt": timestamp
    })


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        filename = body.get("filename")
        filecontent = body.get("filecontent")

        if not filename or not filecontent:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing filename or filecontent"})
            }

        cleaned = clean_csv(filecontent)
        file_id = str(uuid.uuid4())
        s3_key = upload_string(filename, cleaned)
        add_metadata_to_dynamodb(file_id, filename, s3_key)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File uploaded and metadata saved",
                "s3_key": s3_key,
                "file_id": file_id
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
