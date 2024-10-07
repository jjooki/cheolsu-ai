import os

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
    BASE_URL: str = os.getenv("OPENAI_BASE_URL")


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
    PORT: int = int(os.getenv("RDB_PORT", "3306"))
    DATABASE: str = os.getenv("RDB_DATABASE")
    POOL_SIZE: int = int(os.getenv("RDB_POOL_SIZE", "30"))
    
class AuthenticationConfig(BaseConfig):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 20))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))


class Config(BaseConfig):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT_TYPE", EnvironmentType.DEVELOPMENT)
    RELEASE_VERSION: str = os.getenv("RELEASE_VERSION")
    API_PORT: int = int(os.getenv("PORT", 8000))

    # openai
    OPENAI: OpenAIConfig = OpenAIConfig()

    # pinecone
    PINECONE: PineconeConfig = PineconeConfig()

    # mysql
    DATABASE: MysqlConfig = MysqlConfig()
    
    # authentication
    AUTH: AuthenticationConfig = AuthenticationConfig()


config: Config = Config()
