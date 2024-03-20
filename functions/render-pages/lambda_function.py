import boto3
from pdf2image import convert_from_bytes
from os import environ
import logging
from io import BytesIO
import json
from urllib.parse import unquote_plus
from typing import List

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.INFO)

BUCKET_NAME = environ['BUCKET_NAME']
EXTRACT_PAGES_QUEUE_URL = environ['EXTRACT_PAGES_QUEUE_URL']
PAGE_RENDERED_TOPIC_ARN = environ['PAGE_RENDERED_TOPIC_ARN']

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
sns_client = boto3.client('sns')

def load_pdf_as_images(object_key:str, version_id:str=None) -> List[dict]:
  # returns array of images
  params = {"Bucket": BUCKET_NAME, "Key": object_key}
  if version_id:
    params['VersionId'] = version_id
  response = s3_client.get_object(**params)
  return convert_from_bytes(response['Body'].read())


def save_rendered_page_to_bucket(object_key, image):
  
  image_bytes = BytesIO()
  image.save(image_bytes, format="WEBP")
  # Reset the stream position to the beginning
  image_bytes.seek(0)
  # Upload the image data to S3
  s3_client.upload_fileobj(
      Fileobj=image_bytes,
      Bucket=BUCKET_NAME,
      Key=object_key,
      ExtraArgs={
        "ContentType": 'image/webp'
      }
  )
  
  logger.info(f'Saved s3://{BUCKET_NAME}/{object_key}')


def process_pdf(record:dict) -> None:
  
  object_key = unquote_plus(record['s3']['object']['key'])
  owner, upload_id, file_name = object_key.split('/')
  bucket_name = unquote_plus(record['s3']['bucket']['name'])
  version_id = record['s3']['object'].get('versionId')

  logging.info(f"Loading pdf s3://{BUCKET_NAME}/{object_key}")
  
  # Convert PDF pages to images
  for page_index, image in enumerate(load_pdf_as_images(object_key, version_id)):
    
    page_object_key = f"{owner}/{upload_id}/pages/{str(page_index + 1)}.webp"
    
    save_rendered_page_to_bucket(page_object_key, image)
    
    sns_message = {
      "object_key": page_object_key,
      "bucket_name": BUCKET_NAME,
      "version_id": version_id,
      "page": page_index + 1,
      "owner_id": owner,
      "upload_id": upload_id,
      "file_name": file_name
    }
    
    response = sns_client.publish(
      TopicArn=PAGE_RENDERED_TOPIC_ARN,
      Message=json.dumps(sns_message),
    )
    logging.info(response)
    logging.info(f"Rendered image s3://{bucket_name}/{object_key}")
  
  logging.info(f"Extracted pdf s3://{bucket_name}/{object_key}")  


def lambda_handler(event:dict, context:dict) -> dict:
  
  for sqs_record in event['Records']:
      
    try:
        # parse record from 
        s3_event = json.loads(sqs_record['body'])
        for s3_record in s3_event['Records']:
          process_pdf(s3_record)
        # delete the processed message from the SQS queue
        sqs_client.delete_message(
          QueueUrl=EXTRACT_PAGES_QUEUE_URL, 
          ReceiptHandle=sqs_record['receiptHandle']
        )
      
    except Exception: 
        
        logging.error(s3_event) 
        logging.exception("Failed to process record")
      
  return {
    "status": 200,
    "body": 'ok'
  }
