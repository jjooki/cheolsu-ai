#
FROM python:3.12-slim as requirements-stage

#
WORKDIR /tmp

#
RUN pip install poetry

#
COPY ./pyproject.toml ./poetry.lock* /tmp/

#
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

#
FROM python:3.12-slim

#
WORKDIR /code

#
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

#
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
COPY env/.env.dev /code/.env

# 
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--reload", "--loop", "asyncio"]