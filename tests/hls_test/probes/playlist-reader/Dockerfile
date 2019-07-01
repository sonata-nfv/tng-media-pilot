FROM python:3.6-alpine

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip install docker-compose

ENV STREAMING_ENGINE ""
ENV STREAM ""

WORKDIR /app
COPY . /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]
