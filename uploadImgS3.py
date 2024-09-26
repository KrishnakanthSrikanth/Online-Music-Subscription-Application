import json
import requests
import boto3
from botocore.exceptions import ClientError


def uploadImgS3():

    # Create bucket
    client_region = 'us-east-1'
    bucket_name = 's3959200-bucket'

    # Initialize S3 client
    s3_client = boto3.client('s3', region_name=client_region)

    # Checking if bucket exists
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Bucket does not exist, so creating it
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            print("Unexpected error:", e)
            return

    # Reading the data and uploading to s3
    # Load data from a1.json
    with open('a1.json', 'r') as file:
        data = json.load(file)

    # Iterate over each song and download/upload its image
    for song in data['songs']:
        img_url = song['img_url']
        artist_name = song['artist']

        # Download image
        response = requests.get(img_url)
        if response.status_code == 200:
            # Upload image to S3
            s3_client.upload_fileobj(response.raw, bucket_name, f'{artist_name}.jpg')
            print("S3 bucket loaded successfully!!")
        else:
            print(f"Failed to upload image for {artist_name}")


if __name__ == '__main__':
    uploadImgS3()
