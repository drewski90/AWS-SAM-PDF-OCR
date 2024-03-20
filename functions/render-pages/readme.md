# Title: PDF Page Extraction and Image Conversion Lambda

# Description:
This Lambda function extracts pages from a PDF file stored in an S3 bucket, converts each page into an image, and uploads the images back to another S3 bucket. It is triggered by messages in an SQS queue containing information about the PDF files to process.

# Dependencies:
- boto3
- pdf2image

# Environment Variables:
- METADATA_BUCKET_NAME: Name of the S3 bucket where the images will be stored.
- EXTRACT_PAGES_QUEUE_URL: URL of the SQS queue where messages containing PDF file information are received.
- METADATA_CREATED_TOPIC: Topic for notifications about metadata creation.

# Functions:
1. convert_pdf_to_images(bucket_name, object_key, version_id=None)
   - Converts a PDF file from S3 into a list of PIL images.
   - Parameters:
     - bucket_name: Name of the S3 bucket containing the PDF file.
     - object_key: Key of the PDF file in the S3 bucket.
     - version_id: (optional) Version ID of the PDF file.
   - Returns:
     - List of PIL images representing each page of the PDF.

2. upload_images_to_s3(images, output_prefix)
   - Uploads images to an S3 bucket.
   - Parameters:
     - images: List of PIL images to upload.
     - output_prefix: Prefix for the object keys in the destination S3 bucket.
   - Returns: None

3. process_pdf(message)
   - Processes a PDF file stored in S3 by converting it into images and uploading them to S3.
   - Parameters:
     - message: Dictionary containing information about the PDF file (bucket name, object key, version ID, and output prefix).
   - Returns: None

4. lambda_handler(event, context)
   - Main Lambda handler function.
   - Processes messages from an SQS queue, extracts PDF file information, processes the PDF, and deletes the message from the queue.
   - Parameters:
     - event: Event data containing SQS messages.
     - context: Lambda context object.
   - Returns:
     - Dictionary containing the HTTP status and response body.
