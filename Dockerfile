FROM python:3.6.6-alpine3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code/
WORKDIR /code/

RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev

ADD . /code/
RUN pip install --no-cache-dir -r requirements/dev.txt
