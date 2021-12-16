import logging
import sys
from typing import Any
from time import sleep

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

#import queue_helper

logger = logging.getLogger(__name__)

"""
if __debug__:
    ENDPOINT_URL = "http://localhost:4566"
    AWS_REGION = 'us-east-1'
else:
"""    
ENDPOINT_URL = "http://host.docker.internal:4566"
    

AWS_REGION = 'us-east-1'
polling_wait_time = 2 # Long pooling delay in seconds
boto3_config = Config(
    region_name = AWS_REGION,
    s3 = {'addressing_style': 'path'}
)

sqs_client = boto3.client("sqs",
                        aws_access_key_id = 'test',
                        aws_secret_access_key = 'test',
                        config = boto3_config,
                        endpoint_url = ENDPOINT_URL)


#input_queue = sqs_client.get_queue_url(QueueName="simulation-input-queue")
input_queue = ENDPOINT_URL + "/000000000000/simulation-input-queue"


def build_fault_results(exc_info, msg):
    error = exc_info[1]
    logger.error("Source: " + msg)
    print("Source: " + msg)
    print(error)
    """
    if error.args and len(error.agrs > 0):
        for err in error.args:
            logger.error("Error: " + err)
            print(err)
    """

def main():
    queue_not_empty = True
    logger.info("main() is called")
    response: Any
    message: Any
    while queue_not_empty:
        try:
            response = sqs_client.receive_message(
                QueueUrl = input_queue,
                MaxNumberOfMessages = 1,
                WaitTimeSeconds=polling_wait_time
            )
            logger.info("Num of SQS messages: " + str(len(response['Messages'])))

            message = response['Messages'][0]

            #TODO: process message 
            sleep(5.0) #Sleep 5 seconds 

            receipt_handle = message['ReceiptHandle']

            #Delete received message from queue
            sqs_client.delete_message(
                QueueUrl = input_queue,
                ReceiptHandle = receipt_handle
            )
            print('Received and deleted message: %s' % message)
        
        except KeyError:
            queue_not_empty = False
            continue;
        
        except Exception:
            build_fault_results(sys.exc_info(), "Receive sqs message")
               

if __name__ == '__main__':
   main()