import boto3
import os

class AWS:
    def __init__(self,
                 aws_access_key_id: str=None,
                 aws_secret_access_key: str=None,
                 region_name: str=None):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region_name or os.getenv("AWS_REGION")
        )