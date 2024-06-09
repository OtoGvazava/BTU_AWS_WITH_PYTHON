import json
import botocore.session
import http.client

# Initialize the botocore session and clients
session = botocore.session.get_session()
s3 = session.create_client('s3')
dynamodb = session.create_client('dynamodb')
rekognition = session.create_client('rekognition')


def lambda_handler(event, context):
    try:
        # Get the bucket name and object key from the S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_file = response['Body'].read()

        # Prepare the request to the external API
        conn = http.client.HTTPSConnection("carnet.ai")
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        payload = f'--{boundary}\r\nContent-Disposition: form-data; name="imageFile"; filename="{object_key}"\r\nContent-Type: image/jpeg\r\n\r\n'
        payload = payload.encode('utf-8') + image_file + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,ka;q=0.8,ru;q=0.7",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest"
        }

        conn.request("POST", "/recognize-file", body=payload, headers=headers)
        res = conn.getresponse()
        response_data = res.read().decode('utf-8')
        response_json = json.loads(response_data)

        # Check if the response contains the error message
        if response_json.get("error") == "Image doesn't contain a car":
            # Send image to AWS Rekognition
            rekog_response = rekognition.detect_labels(
                Image={
                    'Bytes': image_file
                },
                MaxLabels=10
            )
            # Save the Rekognition response to a different DynamoDB table
            dynamodb.put_item(
                TableName='rekogintionAnalysesDB',
                Item={
                    'rekogintionAnalysesDB': {'S': object_key},
                    'response': {'S': json.dumps(rekog_response)}
                }
            )
        else:
            # Save the response to the original DynamoDB table
            dynamodb.put_item(
                TableName='carnetResponseDB',
                Item={
                    'carnetResponseDB': {'S': object_key},
                    'response': {'S': json.dumps(response_json)}
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }
