FROM python:3.6-alpine

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip install docker-compose

ADD . /app/

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
