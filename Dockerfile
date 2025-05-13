FROM python:3.11.12-alpine3.21

WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


CMD ["fastapi", "run", "app/adapter/inbound/rest/main.py", "--port", "80"]