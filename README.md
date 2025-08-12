# IngestEZ

A serverless pipeline built with AWS Lambda, S3, DynamoDB, and API Gateway to ingest, clean, and store CSV/JSON files. It enables scalable cloud-native file processing with metadata tracking.

---

## Features

- Upload CSV/JSON files via a simple HTTP API  
- Clean and process files inside AWS Lambda  
- Store cleaned files in an S3 bucket  
- Save metadata (file ID, name, S3 key, upload timestamp) in DynamoDB  
- Fully serverless and scalable architecture

---

## Architecture

Client → API Gateway → AWS Lambda → S3 (cleaned files)
↓
DynamoDB (metadata)

---

## Setup

### Prerequisites

- AWS Account  
- AWS CLI installed and configured  
- Python 3.8+ installed  
- `boto3` Python package

### Steps

1. **Create S3 bucket**

```
aws s3 mb s3://<your-bucket-name> --region us-east-1
```

2. **Create DynamoDB table**

```
aws dynamodb create-table \
  --table-name IngestEZUploads \
  --attribute-definitions AttributeName=FileID,AttributeType=S \
  --key-schema AttributeName=FileID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region us-east-1
```

3. **Prepare Lambda deployment package**

- Create folder `lambda_ingestez/`
- Add `lambda_function.py` and `cleaner.py` to it
- Zip contents:
```
cd lambda_ingestez
zip -r ../lambda_ingestez.zip .
```

4. Create IAM role for Lambda

- Attach permissions for S3 (PutObject) and DynamoDB (PutItem)

5. Create Lambda function

- Upload `lambda_ingestez.zip`
- Set handler to `lambda_function.lambda_handler`
- Attach IAM role

6. Create API Gateway HTTP API

- Integrate with Lambda
- Create `POST /upload` route
- Deploy and note the endpoint URL

---

## Project Folder Structure

```
ingestez/
├── lambda_ingestez/
│ ├── lambda_function.py
│ ├── cleaner.py
├── sample.csv
├── upload_clean.py
├── requirements.txt
├── README.md
```

- `lambda_ingestez/` — contains Lambda function code files (lambda_function.py, cleaner.py)
- `sample.csv` — example CSV file for testing
- `upload_clean.py` — your local Python script to upload and clean files (optional)
- `requirements.txt` — Python dependencies (if any)
- `README.md` — project documentation

---

## Usage

Send a POST request to the API endpoint `/upload` with JSON body:

```
{
  "filename": "sample.csv",
  "filecontent": "name,age\nAlice,30\nBob,25"
}
```

Example with `curl`:
```
curl -X POST https://<api-endpoint>/upload \
-H "Content-Type: application/json" \
-d '{"filename":"sample.csv","filecontent":"name,age\nAlice,30\nBob,25"}'
```

---

## License

MIT License

---

## Author

Jay Rajesh Munjapara
