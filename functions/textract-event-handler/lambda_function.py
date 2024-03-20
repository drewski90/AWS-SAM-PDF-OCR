import json
import boto3
from os import environ
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

logger.setLevel(logging.INFO)

METADATA_BUCKET_NAME = environ['METADATA_BUCKET_NAME']
TEXTRACT_STATUS_QUEUE_URL = environ['TEXTRACT_STATUS_QUEUE_URL']

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

def read_s3_json_object(bucket_name, object_key):
  
  logging.info(f"Retrieving object s3://{bucket_name}/{object_key}")
  
  try: 
  
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    
    return json.loads(response['Body'].read())
  
  except ClientError as e:
    
    code = e.response['Error']['Code']
    message = e.response["Error"]['Message']
    
    logging.error(f'Could not retrieve textract part s3://{bucket_name}/{object_key}', exc_info=True)
    
    logging.error(f"{code}: {message}")
    
    raise e
    
  except Exception as e:
    
    logging.error(f'Unhandled error: {str(e)}')
    
    raise e


def remove_none(obj):
  # textract response parser throws an error 
  # if None or null values are present so we'll remove them recursively
  
  if isinstance(obj, dict):
      return {k: remove_none(v) for k, v in obj.items() if v is not None}
  elif isinstance(obj, list):
      return [remove_none(item) for item in obj if item is not None]
  else:
      return obj
    
    
def aggregate_textract_parts(job_id):
  
  output = None
  
  paginator = s3_client.get_paginator('list_objects_v2')

  # Iterate through paginated results
  for page in paginator.paginate(Bucket=METADATA_BUCKET_NAME, Prefix=f'textract_output/{job_id}/'):
    
    if 'Contents' in page:
      # Process objects in the current page
      for obj in page['Contents']:
        
        if not obj["Key"].endswith(".s3_access_check"):
          
          logging.info(f"Processing textract file s3://{METADATA_BUCKET_NAME}/{obj['Key']}")
          
          data = read_s3_json_object(METADATA_BUCKET_NAME, obj['Key'])
          
          if output is None:
            
            output = data
            output['Blocks'] = remove_none(data['Blocks'])
          
          else:
            
            output['Blocks'] += remove_none(data['Blocks'])
    
    else:
      logging.error(f"No objects found in for page {str(page)}")
        
  return output


def handle_record_message(sns_message):
      
  status = sns_message['Status']
  location = sns_message['DocumentLocation']
  object_key = location['S3ObjectName']
  bucket_name = location['S3Bucket']
  output_prefix = sns_message['JobTag']

  if status == "SUCCEEDED":
    
    logging.info(f'Processing textract output for s3://{bucket_name}/{object_key}')
  
    output_key = f"{output_prefix}/textract.json"
      
    output = aggregate_textract_parts(sns_message['JobId'])
    
    s3_client.put_object(
      Bucket=METADATA_BUCKET_NAME,
      Key=output_key,
      Body=json.dumps(output),
      ContentType='application/json'
    )

    logging.info(f'Saved job output to s3://{METADATA_BUCKET_NAME}/{output_key}')
    
  else:
    
    logging.error(f'Discarded message for {object_key} with status of {status}')



def lambda_handler(event, context):
  
  logger.info(event)
  
  for record in event['Records']:
    
    try:
      # parse sns topic message from recieved from sqs queue
      body = json.loads(record['body'])
      # parse sns payload
      sns_message = json.loads(body['Message'])
      # get receiptHandle value to delete the processed sqs message later
      receipt_handle = record['receiptHandle']
      # process the sns message
      handle_record_message(sns_message)
      # delete the processed message from the sqs queue
      sqs_client.delete_message(QueueUrl=TEXTRACT_STATUS_QUEUE_URL, ReceiptHandle=receipt_handle)
    
    except Exception as e:
      
      logging.exception(str(e))
        
  return {
      "status": 200,
      "body": 'ok'
  }