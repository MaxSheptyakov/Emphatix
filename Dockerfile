FROM python:3.10-slim-buster
WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y gcc \
    && pip install --no-cache-dir -r requirements.txt

COPY . .