import argparse
from dotenv import load_dotenv
from s3_utils import *

parser = argparse.ArgumentParser(description='Get bucket name!.')

parser.add_argument('--bucket_name', type=str)

args = parser.parse_args()
bucket_name = args.bucket_name


if __name__ == "__main__":
    load_dotenv()
    s3_client = init_client()
    exists = bucket_exists(s3_client, bucket_name)
    if exists:
        if delete_bucket(s3_client, bucket_name):
            print("Bucket with name {} deleted successfully!".format(bucket_name))
    else:
        print("Bucket with name {} dont exists!".format(bucket_name))