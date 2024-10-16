from typing import List
from app.common.config import config
from app.core.utils.aws import S3

class CharacterService:
    def __init__(self):
        self.s3 = S3(
            aws_access_key_id=config.S3.ACCESS_KEY_ID,
            aws_secret_access_key=config.S3.SECRET_ACCESS_KEY,
            region_name=config.S3.REGION_NAME,
        )
        self.bucket_name = config.S3.BUCKET_NAME
    
    def get_character_image_object(self, key_name: str) -> dict:
        return self.s3.get_object(self.bucket_name, key_name)
    
    def get_character_image_url(self, key_name: str) -> str:
        return self.s3.get_object_url(self.bucket_name, key_name, expiration=config.S3.EXPIRATION)
    
    def _get_character_images(self, character_id: int) -> List[str]:
        images = self.s3.list_objects(
            bucket_name=config.S3.BUCKET_NAME,
            prefix=f"profile/character/{character_id}/"
        )
        profiles_key_names = []
        for content in images.get("Contents", []):
            if content.get("Key").endswith("/"):
                continue
            profiles_key_names.append(content.get("Key"))

        return profiles_key_names
    
    def get_character_image_object_list(self, character_id: int) -> List[dict]:
        images = self._get_character_images(character_id)
        objects = []
        for key_name in images:
            objects.append(self.get_character_image_object(key_name))
            
        return objects
    
    def get_character_image_url_list(self, character_id: int) -> List[str]:
        images = self._get_character_images(character_id)
        urls = []
        for key_name in images:
            urls.append(self.get_character_image_url(key_name))
            
        return urls
    
    def upload_character_image_s3(self, character_id: int, file_name: str, file_path: str) -> dict:
        key_name = f"profile/character/{character_id}/{file_name}"
        return self.s3.upload_file(file_path, self.bucket_name, key_name)
    
    def make_character_prompt(self, prompt: str) -> dict:
        return {
            "role": "system",
            "content ": prompt
        }