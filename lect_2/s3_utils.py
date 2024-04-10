import boto3
from os import getenv
import logging
from botocore.exceptions import ClientError


def init_client():
    try:
        client = boto3.client("s3",
                              aws_access_key_id=getenv("aws_access_key_id"),
                              aws_secret_access_key=getenv("aws_secret_access_key"),
                              aws_session_token=getenv("aws_session_token"),
                              region_name=getenv("aws_region_name")
                              )
        client.list_buckets()

        return client
    except ClientError as e:
        logging.error(e)
    except:
        logging.error("Unexpected error")


def bucket_exists(aws_s3_client, bucket_name):
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def create_bucket(aws_s3_client, bucket_name, region='us-west-2'):
    try:
        location = {'LocationConstraint': region}
        aws_s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_bucket(aws_s3_client, bucket_name):
    try:
        aws_s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_buckets(aws_s3_client):
    try:
        return aws_s3_client.list_buckets()
    except ClientError as e:
        logging.error(e)
        return False