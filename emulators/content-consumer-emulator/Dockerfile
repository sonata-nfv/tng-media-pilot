FROM ubuntu:bionic 

ENV STREAMING_ENGINE ""
ENV STREAM ""
ENV DEBIAN_FRONTEND noninteractive

#RUN apk update && apk add mpv && rm -rf /var/cache/apk/*

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:mc3man/mpv-tests \
    && apt-get update \
    && apt-get install -y --no-install-recommends mpv \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

