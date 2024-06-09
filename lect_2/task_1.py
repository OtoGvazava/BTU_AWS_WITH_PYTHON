import argparse
from dotenv import load_dotenv
from utils.s3_utils import *

parser = argparse.ArgumentParser(description='Get bucket name!.')

parser.add_argument('--bucket_name', type=str)

args = parser.parse_args()
bucket_name = args.bucket_name


if __name__ == "__main__":
    load_dotenv()
    s3_client = init_client()
    exists = bucket_exists(s3_client, bucket_name)
    if exists:
        print("Bucket with name {} is already exists!".format(bucket_name))
    else:
        created = create_bucket(s3_client, bucket_name)
        if created:
            print("Bucket with name '{}' successfully created!".format(bucket_name))
        else:
            print("Problem with creation bucket!")

