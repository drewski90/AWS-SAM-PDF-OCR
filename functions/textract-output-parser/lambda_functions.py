from textractor.parsers import response_parser
import logging
import boto3
import json
from typing import List
from os import environ

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

SQS_INPUT_QUEUE_URL = environ['SQS_INPUT_QUEUE_URL']
SQS_OUTPUT_QUEUE_ARN = environ['SQS_OUTPUT_QUEUE_URL']

def load_document_layout_from_s3(bucket_name, object_key):
  
  # Download the JSON file from S3
  response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
  content = response['Body'].read().decode('utf-8')

  return document_to_layout_data(response_parser(json.loads(content)))

  

def process_s3_event(event):
  
  for record in event['Records']:

    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']
    
    document_layout = load_document_layout_from_s3(bucket_name, object_key)
    
    message_batches = [document_layout[i:i + 10] for i in range(0, len(document_layout), 10)]

    # Publish messages in batches
    for batch in message_batches:
      sqs_messages = []
      for message in batch:
        sqs_messages.append({
          'Id': message['id'],
          'MessageBody': json.dumps(message['body'])
        })
        
    response = sqs_client.send_message_batch(QueueUrl=SQS_OUTPUT_QUEUE_ARN, Entries=sqs_messages)

    # Check for failed messages
    if 'Failed' in response:
      print("Failed to publish some messages:")
      for failed_message in response['Failed']:
        print(f"Message ID: {failed_message['Id']}, Error Code: {failed_message['Code']}, Error Message: {failed_message['Message']}")
    else:
      print("Published batch successfully")


def lambda_handler(event, context):
  
  logger.info(event)

  for record in event['Records']:
      
    try:
        # get sns payload from sqs record
        body = json.loads(record['body'])
        # parse sns message from the payload
        s3_event = json.loads(body['Message'])
        # get reciept handle to delete the record once it has been processed
        receipt_handle = record['receiptHandle']
        process_s3_event(s3_event)
        # delete the processed message from the SQS queue
        sqs_client.delete_message(QueueUrl=SQS_INPUT_QUEUE_URL, ReceiptHandle=receipt_handle)
      
    except Exception as e:
        
      logging.error(f'Record processing failed: {str(e)}')
  
  
def document_to_layout_data(document) -> List[dict]:
  
  output = []
  
  for page_index, page in enumerate(document.pages):
    
    for layout_index, layout in enumerate(page.layouts):
      
      bbox = layout.bbox
      
      item = {
        "type": layout.layout_type,
        "bbox": {
          'x': bbox.x, 
          "y": bbox.y, 
          "width": bbox.width, 
          "height": bbox.height
        },
        "confidence": layout.confidence,
        "metadata": layout.metadata,
        "content": layout.to_markdown(),
        "id": layout.id,
        "page": page_index,
        "order": layout_index
      }
      
      output.append(item)
      logging.info(f"Detected {item['type']} on page {page_index}")
      
  return output