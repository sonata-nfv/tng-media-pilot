FROM python:3.6-alpine

RUN apk add --update \
    openssl-dev \
    libffi-dev \
    alpine-sdk \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip3 install --upgrade \
    setuptools \
    docker-compose

ADD . /app/

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]