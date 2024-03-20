# Title: Textract Job Starter Lambda

# Description:
This Lambda function initiates a Textract job for analyzing documents stored in an S3 bucket. It listens for messages in an SQS queue, extracts information about the documents, starts Textract jobs for each document, and deletes the processed messages from the queue.

# Dependencies:
- boto3
- botocore
- json

# Environment Variables:
- START_TEXTRACT_JOB_QUEUE_URL: URL of the SQS queue where messages containing document information are received.
- TEXTRACT_STATUS_TOPIC_ARN: ARN of the SNS topic for Textract job status notifications.
- TEXTRACT_SNS_ROLE_ARN: ARN of the IAM role for Textract to publish notifications to SNS.
- METADATA_BUCKET_NAME: Name of the S3 bucket where Textract output will be stored.

# Functions:
1. start_textract_job(message)
   - Initiates a Textract job for analyzing a document stored in an S3 bucket.
   - Parameters:
     - message: Dictionary containing information about the document (bucket name, object key, version ID, and message ID).
   - Returns: None

2. lambda_handler(event, context)
   - Main Lambda handler function.
   - Processes messages from an SQS queue, extracts document information, starts Textract jobs, and deletes the processed messages from the queue.
   - Parameters:
     - event: Event data containing SQS messages.
     - context: Lambda context object.
   - Returns:
     - Dictionary containing the HTTP status and response body.
