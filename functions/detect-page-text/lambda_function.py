import boto3
from PIL import Image
import io
import json
from os.path import dirname, splitext, basename
from textractor.parsers import response_parser
import logging
from os import environ

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
textract_client = boto3.client('textract')
TESSERACT_QUEUE = environ['INPUT_QUEUE']


def read_image(bucket_name:str, object_key:str) -> Image:
    # Retrieve image data from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    # pull into memory
    image_data = io.BytesIO(response['Body'].read())
    image_data.seek(0)
    # Open image using PIL
    return Image.open(image_data)


def image_to_textractor(pil_image:Image):
    # convert a image to a textractor document
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    response = textract_client.analyze_document(
        Document={'Bytes': img_byte_arr.read()},
        FeatureTypes=['TABLES', 'FORMS']
    )
    return response_parser.parse(response)


def extract_text_from_s3_image(bucket_name:str, object_key:str) -> str:
    # Retrieve image data from S3
    image = read_image(bucket_name, object_key)
    document = image_to_textractor(image)
    return document.to_markdown()


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
        output_key = f"{dirname(object_key)}/{splitext(basename(object_key))[0]}.textract"
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

  
