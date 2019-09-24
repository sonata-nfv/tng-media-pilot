
FROM sjourdan/ffprobe:latest

RUN apk add --update \
    py-pip \
    python-dev \
    libffi-dev \
    openssl-dev \
    gcc \
    libc-dev \
    make \
    && rm -rf /var/cache/apk/*

RUN pip install cffi && pip install docker-compose

ENV STREAMING_ENGINE ""
ENV STREAM ""

WORKDIR /app
COPY . /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
