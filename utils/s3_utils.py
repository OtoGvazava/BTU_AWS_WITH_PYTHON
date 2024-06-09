import random
from hashlib import md5
from time import localtime

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


def download_file_and_upload_to_s3(aws_s3_client, bucket_name, url, file_name, keep_local=False):
    from urllib.request import urlopen
    import io
    with urlopen(url) as response:
        content = response.read()
        try:
            aws_s3_client.upload_fileobj(Fileobj=io.BytesIO(content), Bucket=bucket_name, Key=file_name)
        except Exception as e:
            logging.error(e)

    if keep_local:
        with open(file_name, 'wb') as jpg_file:
            jpg_file.write(content)
    return "https://s3-{0}.amazonaws.com/{1}/{2}".format("uz-west-2", bucket_name, file_name)


def upload_images_to_s3_recursive(s3_client, bucket_name, image_urls):
    if len(image_urls) != 0:
        file_name = f'image_file_{md5(str(localtime()).encode("utf-8")).hexdigest()}.jpg'
        download_file_and_upload_to_s3(s3_client, bucket_name, image_urls[0], file_name)
        image_urls.pop(0)
        upload_images_to_s3_recursive(s3_client, bucket_name, image_urls)


def set_object_access_policy(aws_s3_client, bucket_name, file_name):
    try:
        response = aws_s3_client.put_object_acl(
            ACL="public-read",
            Bucket=bucket_name,
            Key=file_name
        )
    except ClientError as e:
        logging.error(e)
        return False
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def generate_public_read_policy(bucket_name):
    import json
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    return json.dumps(policy)


def create_bucket_policy(aws_s3_client, bucket_name):
    aws_s3_client.put_bucket_policy(
        Bucket=bucket_name, Policy=generate_public_read_policy(bucket_name)
    )
