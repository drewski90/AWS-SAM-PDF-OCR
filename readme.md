# Features

The scalable Optical Character Recognition (OCR) stack efficiently extracts individual pages into WebP images, optimizing for minimal storage footprint. By default, the stack incorporates two OCR systems: AWS Textract and Google's Tesseract. While Tesseract proves to be cost-effective, Textract demonstrates superior accuracy, thus ensuring optimal results while maintaining cost-efficiency.

# Stack Components

## PDFProcessingQueue

An SQS queue named pdf-processing-queue for processing PDF documents.

## QueuesPolicy

An SQS queue policy allowing messages to be sent to specific queues.

## PDFBucket

An S3 bucket for storing PDF documents with server-side encryption and notification configuration to trigger processing.

## DeadLetter

An SQS queue for handling dead-letter messages.

## PageRenderedTopic

An SNS topic for notifying when pages are rendered.

## RenderPagesHandler

A Lambda function for rendering pages from PDF documents.

## TesseractTextDetectQueue

An SQS queue for Tesseract text detection.

## TesseractTextDetect

A Lambda function for Tesseract text detection.

## DetectPageTextQueue

An SQS queue for detecting text on processed pages.

## DetectPageText

A Lambda function for detecting text on processed pages.

## Usage

Once the stack is deployed, you can start using it to process PDF documents. PDF documents uploaded to the specified S3 bucket (PDFBucket) will trigger the processing functions.

### NOTE

Object keys are expected to conform to the following format:

f"{object_owner}\\{unique_upload_id}\\{filename}.pdf"

## Monitoring and Logs

Logs for the Lambda functions are stored in AWS CloudWatch Logs. You can monitor and analyze logs through the AWS Management Console or using the AWS CLI.

### Cleanup

Log retention is set to 7 days