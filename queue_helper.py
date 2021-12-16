import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
sqs = boto3.resource('sqs')

sqs = boto3.resource('sqs', )
message_queue = "simulation-input-queue"
#queue_name = "http://localhost:4566/000000000000/simulation-input-queue"
queue_name = "http://host.docker.internal:4566/000000000000/simulation-input-queue"
polling_wait_time = 2 #Polling wait time in seconds 

if __debug__:
    ENDPOINT_URL = "http://host.docker.internal:4566"
    AWS_REGION = 'us-east-1'
else:
    ENDPOINT_URL = "s3://oxford-chemistry/input/"