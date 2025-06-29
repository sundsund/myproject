import json
import boto3
import csv
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}, Key: {key}")

    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        # Get the object data as a string
        data = response['Body'].read().decode('utf-8')

        # Process the data
        reader = csv.reader(io.StringIO(data))
        next(reader)  # Skip header row
        for row in reader:
            print(f"Year: {row[0]}, Mileage: {row[1]}, Price: {row[2]}")

        return {
            'statusCode': 200,
            'body': json.dumps('File processed successfully!')
        }
    except Exception as e:
        print(e) # Print the exception for logging
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing file: {str(e)}')
        }
