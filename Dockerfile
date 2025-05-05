FROM python:3.11.12-alpine3.21

WORKDIR /app

COPY requirements.txt .

COPY src .

RUN pip install -r requirements.txt