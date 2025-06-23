# Stage 1: Build
FROM python:3.11.12-alpine3.21 AS builder

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && pip freeze > /code/requirements.lock

# Stage 2: Runtime
FROM python:3.11.12-alpine3.21

WORKDIR /code

COPY --from=builder /code/requirements.lock /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic.ini /code/alembic.ini
COPY ./app /code/app
