FROM alfg/ffmpeg

RUN apk add --update \
    py-pip\
    && rm -rf /var/cache/apk/*

RUN pip install docker-compose==1.23.2

ENV AGGREGATOR ""
ENV STREAM ""
ENV VIDEO ""

WORKDIR /app

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

