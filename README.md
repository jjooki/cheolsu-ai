# cheolsu-ai
=======
## How to run in local environment
1. You must add `.env.local` file in `/env` directory. Environments format is below.
2. run docker compose command like this.
```bash
sh scripts/local.startup.sh && \
  docker compose -f docker-compose.local.yaml up --build -d
```
=======
## Environment Sample

```bash
# API Server Config
ENVIRONMENT_TYPE=dev
RELEASE_VERSION="0.1.0"
PORT=8000

# mysql database
RDB_HOST=localhost
RDB_RO_HOST=localhost
RDB_USERNAME=user
RDB_PASSWORD=password
RDB_PORT=3306
RDB_DATABASE=database
RDB_POOL_SIZE=10

# MongoDB
MONGODB_CONNECTION_STRING=mongodb+srv://***:***@**.*****.mongodb.net/

# Auth
JWT_SECRET_KEY=****
JWT_REFRESH_SECRET_KEY=****
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10
REFRESH_TOKEN_EXPIRE_MINUTES=10

# OpenAI
OPENAI_API_KEY=sk-****
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_COMPLETION_MODEL=gpt-3.5-turbo-instruct
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```