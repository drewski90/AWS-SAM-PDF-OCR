# AWS Lambda Function for Text Extraction from Images

This AWS Lambda function is designed to extract text from images stored in an S3 bucket using Amazon Textract and save the extracted text back to the S3 bucket. The function is triggered by messages from an SQS queue containing information about the images to be processed.

## Functionality

- **read_image**: Retrieves image data from an S3 bucket and opens it using the Pillow library.
- **image_to_textractor**: Converts the image to a format compatible with Amazon Textract and sends it for text analysis.
- **extract_text_from_s3_image**: Combines the above functions to extract text from images stored in S3.
- **save_image_text**: Saves the extracted text back to the S3 bucket.
- **lambda_handler**: Main Lambda function handler that processes SQS messages, extracts text from images, and saves the results.

## Dependencies

- **boto3**: AWS SDK for Python.
- **Pillow**: Python Imaging Library for opening, manipulating, and saving many different image file formats.
- **textract**: Python package for interacting with Amazon Textract.
- **json**: Python library for JSON data manipulation.
- **os**: Python library for interacting with the operating system.
- **io**: Python library for handling I/O operations.

## Environment Variables

- **INPUT_QUEUE**: Name of the SQS queue where messages triggering the Lambda function are sent.

## Usage

1. Ensure that the necessary IAM permissions are granted to the Lambda function to access S3, SQS, and Textract.
2. Set up an SQS queue to trigger the Lambda function.
3. Configure the Lambda function with the required environment variables and trigger source (SQS queue).
4. Deploy the Lambda function using the AWS Management Console or the AWS CLI.

## Deployment

Deploy the Lambda function using AWS CloudFormation or the AWS Management Console. Make sure to properly configure the function's trigger, environment variables, and permissions.

## Error Handling

The function logs errors and exceptions encountered during processing to CloudWatch Logs. Monitoring and alerting can be set up using AWS CloudWatch Alarms.

## License

This project is licensed under the [MIT License](LICENSE).
