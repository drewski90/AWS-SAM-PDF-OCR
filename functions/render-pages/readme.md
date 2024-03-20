# AWS Lambda Function for Processing PDFs and Rendering Pages to WebP Images

This AWS Lambda function processes PDF documents uploaded to an S3 bucket, converts each page to a WebP image, and saves the rendered images back to the bucket. The function is triggered by messages from an SQS queue containing information about the PDF files to be processed.

## Functionality

- **load_pdf_as_images**: Loads a PDF file from an S3 bucket and converts each page to a WebP image using pdf2image library.
- **save_rendered_page_to_bucket**: Saves the rendered WebP image back to the S3 bucket.
- **process_pdf**: Processes each page of the PDF file, converts it to a WebP image, and publishes a message to an SNS topic with information about the rendered page.
- **lambda_handler**: Main Lambda function handler that processes SQS messages, extracts PDF files, renders pages, and publishes messages to SNS.

## Dependencies

- **boto3**: AWS SDK for Python.
- **pdf2image**: Python library for converting PDF pages to images.
- **json**: Python library for JSON data manipulation.
- **os**: Python library for interacting with the operating system.
- **io**: Python library for handling I/O operations.
- **urllib**: Python library for URL handling.
- **logging**: Python library for logging.

## Environment Variables

- **BUCKET_NAME**: Name of the S3 bucket where PDF files are stored.
- **EXTRACT_PAGES_QUEUE_URL**: URL of the SQS queue where messages triggering the Lambda function are sent.
- **PAGE_RENDERED_TOPIC_ARN**: ARN of the SNS topic where messages about rendered pages are published.

## Usage

1. Ensure that the necessary IAM permissions are granted to the Lambda function to access S3, SQS, and SNS.
2. Set up an SQS queue to trigger the Lambda function.
3. Configure the Lambda function with the required environment variables and trigger source (SQS queue).
4. Deploy the Lambda function using the AWS Management Console or the AWS CLI.

## Deployment

Deploy the Lambda function using AWS CloudFormation or the AWS Management Console. Make sure to properly configure the function's trigger, environment variables, and permissions.

## Error Handling

The function logs errors and exceptions encountered during processing to CloudWatch Logs. Monitoring and alerting can be set up using AWS CloudWatch Alarms.

## License

This project is licensed under the [MIT License](LICENSE).
