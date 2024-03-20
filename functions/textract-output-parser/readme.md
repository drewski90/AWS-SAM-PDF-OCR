# Title: Textract Document Parser and Message Publisher Lambda

# Description:
This Lambda function parses documents extracted by Textract, processes the layout data, and publishes messages containing layout information to an SQS queue. It listens for S3 events triggered by the arrival of new documents, retrieves the layout data from S3, processes it, and sends messages to an SQS output queue.

Dependencies:
- textractor (custom module)
- boto3
- json
- logging
- typing

# Environment Variables:
- SQS_INPUT_QUEUE_URL: URL of the SQS queue where S3 event messages are received.
- SQS_OUTPUT_QUEUE_ARN: ARN of the SQS queue where layout information messages will be published.

# Functions:
1. load_document_layout_from_s3(bucket_name, object_key)
   - Loads document layout data from a JSON file stored in an S3 bucket.
   - Parameters:
     - bucket_name: Name of the S3 bucket containing the JSON file.
     - object_key: Key of the JSON file in the S3 bucket.
   - Returns:
     - List of dictionaries containing layout data.

2. process_s3_event(event)
   - Processes S3 events triggered by the arrival of new documents.
   - Loads document layout data from S3, processes it, and sends messages containing layout information to an SQS queue.
   - Parameters:
     - event: Event data containing S3 event records.
   - Returns: None

3. lambda_handler(event, context)
   - Main Lambda handler function.
   - Processes messages from an SQS queue, extracts S3 event data, processes the document layout, sends messages to an SQS output queue, and deletes the processed messages from the input queue.
   - Parameters:
     - event: Event data containing SQS messages.
     - context: Lambda context object.
   - Returns: None

4. document_to_layout_data(document) -> List[dict]
   - Converts Textract document layout data into a list of dictionaries.
   - Parameters:
     - document: Textract document object containing layout data.
   - Returns:
     - List of dictionaries containing layout information for each page and layout detected in the document.
