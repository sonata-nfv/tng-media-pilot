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

ENTRYPOINT ["/app/entrypoint.sh"]

