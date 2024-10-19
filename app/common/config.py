import os
import pytz

from dotenv import load_dotenv
from enum import Enum
from pydantic.v1 import BaseSettings
from nest_asyncio import apply

apply()
load_dotenv(override=True)

class EnvironmentType(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True

class OpenAIConfig(BaseConfig):
    API_KEY: str = os.getenv("OPENAI_API_KEY")
    CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL")
    COMPLETION_MODEL: str = os.getenv("OPENAI_COMPLETION_MODEL")
    EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL")
    IMAGE_MODEL: str = os.getenv("OPENAI_IMAGE_MODEL")
    BASE_URL: str = os.getenv("OPENAI_BASE_URL")
    RETRY: int = int(os.getenv("OPENAI_RETRY", "3"))
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")

class PineconeConfig(BaseConfig):
    INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")
    NAMESPACE: str = os.getenv("PINECONE_NAMESPACE")
    API_KEY: str = os.getenv("PINECONE_API_KEY")
    HOST: str = os.getenv("PINECONE_HOST")

class MysqlConfig(BaseConfig):
    HOST: str = os.getenv("RDB_HOST")
    RO_HOST: str = os.getenv("RDB_RO_HOST")
    USERNAMES: str = os.getenv("RDB_USERNAME")
    PASSWORD: str = os.getenv("RDB_PASSWORD")
    DB_PORT: int = 3306
    DATABASE: str = os.getenv("RDB_DATABASE")
    POOL_SIZE: int = int(os.getenv("RDB_POOL_SIZE", "30"))

class MongoDBConfig(BaseConfig):
    CONNECTION_STRING: str = os.getenv("MONGODB_CONNECTION_STRING")

class RedisConfig(BaseConfig):
    HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    DB: int = int(os.getenv("REDIS_DB", "0"))
    MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
    REDISMOD_HOST: str = os.getenv("REDISMOD_HOST", "redismod")
    
class AuthenticationConfig(BaseConfig):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 20))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

class S3Config(BaseConfig):
    BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
    ACCESS_KEY_ID: str = os.getenv("S3_ACCESS_KEY_ID")
    SECRET_ACCESS_KEY: str = os.getenv("S3_SECRET_ACCESS_KEY")
    REGION_NAME: str = os.getenv("S3_REGION_NAME")
    EXPIRATION: int = int(os.getenv("S3_EXPIRATION", 10800))    
    
class Config(BaseConfig):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT_TYPE", EnvironmentType.DEVELOPMENT)
    RELEASE_VERSION: str = os.getenv("RELEASE_VERSION")
    API_PORT: int = int(os.getenv("PORT", 8000))
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Seoul")

    # openai
    OPENAI: OpenAIConfig = OpenAIConfig()

    # pinecone
    PINECONE: PineconeConfig = PineconeConfig()

    # mysql
    DATABASE: MysqlConfig = MysqlConfig()
    
    # authentication
    AUTH: AuthenticationConfig = AuthenticationConfig()
    
    # mongodb
    MONGODB: MongoDBConfig = MongoDBConfig()
    
    # redis
    CACHE: RedisConfig = RedisConfig()
    
    # s3
    S3: S3Config = S3Config()


config: Config = Config()
