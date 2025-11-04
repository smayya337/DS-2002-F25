import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'ds2002-f25-eav6vg'
local_file_path = 'PlaneWaitingAtDoha.jpg'
s3_key = 'qatarairways.jpg' # Example of a different key

s3.upload_file(
    Filename=local_file_path,  # The local file path on your system
    Bucket=bucket,             # The S3 bucket name
    Key=s3_key                 # The destination object key in S3
)
