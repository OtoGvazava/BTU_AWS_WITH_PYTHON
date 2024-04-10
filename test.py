import boto3
from os import getenv
import logging
from botocore.exceptions import ClientError
from hashlib import md5
from time import localtime
from dotenv import load_dotenv

load_dotenv()


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


def list_buckets(aws_s3_client):
    try:
        return aws_s3_client.list_buckets()
    except ClientError as e:
        logging.error(e)
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


if __name__ == "__main__":
    s3_client = init_client()
    print(download_file_and_upload_to_s3(s3_client,
                                         "new-bucket0.6252182644760979",
                                         "https://smaller-pictures.appspot.com/images/dreamstime_xxl_65780868_small.jpg",
                                         f'image_file_{md5(str(localtime()).encode("utf-8")).hexdigest()}.jpg',
                                         keep_local=True))

    # for i in range(10):
    #   print("created bucket status: {}".format(create_bucket(s3_client, "new-bucket" + str(random.random()))))

    # buckets = list_buckets(s3_client)

    # if buckets:
    #   for bucket in buckets['Buckets'][:10]:
    #     delete_bucket(s3_client, bucket['Name'])

    # if buckets:
    #   for bucket in buckets[u'Buckets']:
    #     print(bucket["Name"])
    #     print(bucket["CreationDate"])