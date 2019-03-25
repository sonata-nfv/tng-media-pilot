FROM sjourdan/ffprobe:latest

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip install docker-compose

ENV STREAMING_ENGINE ""
ENV STREAM ""

WORKDIR /app
COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
