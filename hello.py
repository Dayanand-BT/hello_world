import boto3
import os
from PIL import Image
import io
import sys

def preprocess_image(bucket_name, object_key):
    s3 = boto3.client('s3')
    
    # Download image from S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(e)
        return "Error downloading image from S3"
    
    # Open image using PIL
    try:
        image = Image.open(io.BytesIO(response['Body'].read()))
    except Exception as e:
        print(e)
        return "Error opening image"
    
    # Convert image to grayscale
    grayscale_image = image.convert('L')

    # Save grayscale image to a temporary file
    temp_file = '/tmp/grayscale_image.jpg'  # or any other format supported by PIL
    grayscale_image.save(temp_file)

    # Upload processed image back to S3
    try:
        s3.upload_file(Filename=temp_file, Bucket=bucket_name, Key='grayscale_images/' + object_key)
    except Exception as e:
        print(e)
        return "Error uploading processed image to S3"

    return "Grayscale image processed and saved to S3 bucket 'grayscale_images'"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python preprocess_image.py <bucket_name> <object_key>")
        sys.exit(1)
    bucket_name = sys.argv[1]
    object_key = sys.argv[2]
    result = preprocess_image(bucket_name, object_key)
    print(result)
