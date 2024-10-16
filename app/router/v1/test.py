from fastapi import FastAPI, Response, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = FastAPI()

# S3 클라이언트 설정
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_AWS_ACCESS_KEY',
    aws_secret_access_key='YOUR_AWS_SECRET_KEY',
    region_name='YOUR_AWS_REGION'
)

# 버킷 이름 설정
BUCKET_NAME = 'your-s3-bucket-name'

@app.get("/image/{image_key}")
async def get_s3_image(image_key: str):
    try:
        # S3에서 파일 가져오기
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=image_key)
        file_content = s3_object['Body'].read()

        # 이미지 반환 (JPEG로 가정, 필요 시 변경)
        return Response(content=file_content, media_type="image/jpeg")

    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Image not found in S3 bucket")
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="S3 credentials error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")