FROM alfg/ffmpeg

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip install docker-compose

ENV AGGREGATOR ""
ENV STREAM ""

ARG video
ENV VIDEO=$video

WORKDIR /app

COPY $VIDEO /app
COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

