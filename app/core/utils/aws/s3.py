import logging

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException, Response

from .base import AWS

logger = logging.getLogger(__name__)

class S3(AWS):
    def __init__(self,
                 aws_access_key_id: str=None,
                 aws_secret_access_key: str=None,
                 region_name: str=None):
        ## `secretmanager:GetSecretValue` IAM role is required to run this code
        super().__init__(aws_access_key_id,
                         aws_secret_access_key,
                         region_name)
        self.client = self.session.client("s3")
    
    def list_objects(self, bucket_name: str, max_keys: int=1000, prefix: str=None):
        return self.client.list_objects_v2(
            Bucket=bucket_name,
            MaxKeys=max_keys,
            Prefix=prefix
        )
    
    def upload_file(self,
                    file_path: str,
                    bucket_name: str,
                    object_key: str) -> bool:
        """
        Upload a file to an S3 bucket.

        :param file_path: File to upload.
        :param bucket_name: Bucket to upload to.
        :param object_key: S3 object key. If not specified then file_name is used.
        :return: True if file was uploaded, else False.
        """
        if object_key is None:
            object_key = os.path.basename(file_path)
            
        try:
            self.client.upload_file(file_path, bucket_name, object_key)
            
        except ClientError as e:
            logging.error(e)
            return False
        
        return True
    
    def download_file(self, bucket_name: str, object_key: str, file_path: str):
        """
        Download a file from an S3 bucket.

        :param bucket_name: Bucket to download from.
        :param object_key: S3 object key.
        :param file_path: File to download to.
        :return: True if file was downloaded, else False.
        """
        try:
            self.client.download_file(bucket_name, object_key, file_path)
            
        except ClientError as e:
            logging.error(e)
            return False
        
        return True
    
    def get_object(self, bucket_name: str, object_key: str) -> dict:
        try:
            # S3에서 파일 가져오기
            s3_object = self.client.get_object(Bucket=bucket_name, Key=object_key)
            file_content = s3_object['Body'].read()
            media_type = object_key.split('.')[-1]

            # 이미지 반환 (JPEG로 가정, 필요 시 변경)
            return {
                "object_key": object_key,
                "content": file_content,
                "media_type": f"image/{media_type}"
            }

        except self.client.exceptions.NoSuchKey:
            raise HTTPException(status_code=404, detail="Image not found in S3 bucket")
        except (NoCredentialsError, PartialCredentialsError):
            raise HTTPException(status_code=500, detail="S3 credentials error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    def get_object_url(self, bucket_name: str, object_key: str, expiration: int=3600) -> str:
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            return response
        
        except self.client.exceptions.NoSuchKey:
            raise HTTPException(status_code=404, detail="Image not found in S3 bucket")
        except (NoCredentialsError, PartialCredentialsError):
            raise HTTPException(status_code=500, detail="S3 credentials error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        