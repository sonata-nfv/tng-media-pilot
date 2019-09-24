FROM python:3.6-alpine

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*
    
RUN pip install docker-compose==1.23.2

ADD . /app/

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
