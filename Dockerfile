FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;
RUN mkdir /pet_api
WORKDIR /pet_api

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /pet_api/
COPY ./pet_api /pet_api

COPY ./SQLModel.sql /docker-entrypoint-initdb.d/SQLModel.sql