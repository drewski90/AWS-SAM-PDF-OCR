# Title: Textract Output Aggregator Lambda

# Description:
This Lambda function aggregates Textract output parts from an S3 bucket, processes them, and saves the aggregated output as a JSON file back to the S3 bucket. It listens for messages in an SQS queue containing information about Textract job statuses, retrieves the output parts from the S3 bucket, aggregates them, and saves the aggregated output.

# Dependencies:
- boto3
- json
- logging
- botocore

# Environment Variables:
- METADATA_BUCKET_NAME: Name of the S3 bucket where Textract output and metadata are stored.
- TEXTRACT_STATUS_QUEUE_URL: URL of the SQS queue where Textract job status messages are received.

# Functions:
1. read_s3_json_object(bucket_name, object_key)
   - Reads a JSON object from an S3 bucket.
   - Parameters:
     - bucket_name: Name of the S3 bucket.
     - object_key: Key of the JSON object in the S3 bucket.
   - Returns:
     - JSON object loaded from the S3 object.

2. remove_none(obj)
   - Recursively removes None or null values from a dictionary or list.
   - Parameters:
     - obj: Dictionary or list to be processed.
   - Returns:
     - Dictionary or list with None or null values removed.

3. aggregate_textract_parts(job_id)
   - Aggregates Textract output parts from an S3 bucket for a given job ID.
   - Parameters:
     - job_id: ID of the Textract job.
   - Returns:
     - Aggregated Textract output as a JSON object.

4. handle_record_message(sns_message)
   - Processes a Textract job status message received from an SQS queue.
   - Retrieves Textract output parts from the S3 bucket, aggregates them, and saves the aggregated output.
   - Parameters:
     - sns_message: Dictionary containing information about the Textract job status.
   - Returns: None

5. lambda_handler(event, context)
   - Main Lambda handler function.
   - Processes messages from an SQS queue, extracts Textract job status information, aggregates Textract output parts, saves the aggregated output to the S3 bucket, and deletes the processed messages from the queue.
   - Parameters:
     - event: Event data containing SQS messages.
     - context: Lambda context object.
   - Returns:
     - Dictionary containing the HTTP status and response body.
