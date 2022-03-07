FROM python:3.8.5-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add zlib alpine-sdk postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev cargo zlib-dev jpeg-dev

COPY ./requirements.txt .

# copy favicon
COPY ./static/img/favicon.ico .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install gunicorn

COPY . .
