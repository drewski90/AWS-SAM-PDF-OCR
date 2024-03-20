import boto3
import pytesseract
from PIL import Image
import io
import json
from os.path import dirname, splitext, basename
import logging
from os import environ

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
TESSERACT_QUEUE = environ['INPUT_QUEUE']

def extract_text_from_s3_image(bucket_name:str, object_key:str):
    # Retrieve image data from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    # pull into memory
    image_data = io.BytesIO(response['Body'].read())
    image_data.seek(0)
    # Open image using PIL
    image = Image.open(image_data)
    # Perform OCR using Pytesseract
    text = pytesseract.image_to_string(image)
    return text
  
def save_image_text(bucket:str, key:str, text:str):
  
  return s3_client.put_object(
    Bucket=bucket, 
    Key=key, 
    Body=text
  )


def lambda_handler(event:dict, context:dict) -> dict:
  
  for sqs_record in event['Records']:
      
    try:
        # parse record from 
        body = json.loads(sqs_record['body'])
        payload = json.loads(body['Message'])
        object_key = payload['object_key']
        bucket_name = payload['bucket_name']
        image_text = extract_text_from_s3_image(bucket_name, object_key)
        output_key = f"{dirname(object_key)}/{splitext(basename(object_key))[0]}.tesseract"
        save_image_text(bucket_name, output_key, image_text)
        # delete the processed message from the SQS queue
        sqs_client.delete_message(
          QueueUrl=TESSERACT_QUEUE, 
          ReceiptHandle=sqs_record['receiptHandle']
        )
      
    except Exception: 
        
        logging.error(body) 
        logging.exception("Failed to process record")
      
  return {
    "status": 200,
    "body": 'ok'
  }

  
