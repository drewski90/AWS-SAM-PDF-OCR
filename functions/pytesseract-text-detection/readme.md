# AWS Lambda Function for Text Extraction from Images using Pytesseract

This AWS Lambda function is designed to extract text from images stored in an S3 bucket using Pytesseract, an optical character recognition (OCR) tool for Python. The function is triggered by messages from an SQS queue containing information about the images to be processed.

## Functionality

- **extract_text_from_s3_image**: Retrieves image data from an S3 bucket, performs OCR using Pytesseract, and returns the extracted text.
- **save_image_text**: Saves the extracted text back to the S3 bucket.
- **lambda_handler**: Main Lambda function handler that processes SQS messages, extracts text from images, and saves the results.

## Dependencies

- **boto3**: AWS SDK for Python.
- **pytesseract**: Python wrapper for Google's Tesseract-OCR Engine.
- **Pillow**: Python Imaging Library for opening, manipulating, and saving many different image file formats.
- **json**: Python library for JSON data manipulation.
- **os**: Python library for interacting with the operating system.
- **io**: Python library for handling I/O operations.

## Environment Variables

- **INPUT_QUEUE**: Name of the SQS queue where messages triggering the Lambda function are sent.

## Usage

1. Ensure that the necessary IAM permissions are granted to the Lambda function to access S3 and SQS.
2. Set up an SQS queue to trigger the Lambda function.
3. Configure the Lambda function with the required environment variable and trigger source (SQS queue).
4. Deploy the Lambda function using the AWS Management Console or the AWS CLI.

## Deployment

Deploy the Lambda function using AWS CloudFormation or the AWS Management Console. Make sure to properly configure the function's trigger, environment variable, and permissions.

## Error Handling

The function logs errors and exceptions encountered during processing to CloudWatch Logs. Monitoring and alerting can be set up using AWS CloudWatch Alarms.

## License

This project is licensed under the [MIT License](LICENSE).
