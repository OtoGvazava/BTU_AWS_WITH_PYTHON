from dotenv import load_dotenv
from utils.s3_utils import init_client, upload_images_to_s3_recursive, create_bucket_policy
import asyncio
from utils.myautoutils import get_my_auto_image_urls
import argparse


def main():
    parser = argparse.ArgumentParser(description='MyAuto car image recognition!.')

    parser.add_argument('--set_policy', type=bool)
    args = parser.parse_args()
    set_policy = args.set_policy

    bucket_name = "myautootiko"
    load_dotenv()
    s3_client = init_client()
    asyncio.set_event_loop(asyncio.new_event_loop())
    no_car_image = "https://static.my.ge/myhome/photos/7/6/0/4/7/large/16774067_4.jpg";
    image_urls = asyncio.get_event_loop().run_until_complete(get_my_auto_image_urls())
    if set_policy:
        create_bucket_policy(s3_client, bucket_name)
    image_urls.append(no_car_image)
    upload_images_to_s3_recursive(s3_client, bucket_name, image_urls)


if __name__ == "__main__":
    main()
