import boto3
import requests

local_file_path = "CCDCTeam2025.jpg"
bucket = "ds2002-f25-eav6vg"
s3_key = local_file_path

s3 = boto3.client('s3', region_name="us-east-1")

response = requests.get("https://uvacns.com/images/CCDCTeam2025.jpg")
with open(local_file_path, "wb") as f:
    f.write(response.content)

s3.upload_file(
    Filename=local_file_path,  # The local file path on your system
    Bucket=bucket,             # The S3 bucket name
    Key=s3_key                 # The destination object key in S3
)


presigned = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': s3_key},
    ExpiresIn=604800
)

print(f"Presigned URL: {presigned}")
