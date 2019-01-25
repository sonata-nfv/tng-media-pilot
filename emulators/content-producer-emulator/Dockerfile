FROM ubuntu:trusty

ENV AGGREGATOR ""
ENV APP ""
ENV STREAM ""

ARG video
ENV VIDEO=$video

RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:mc3man/trusty-media -y
RUN apt-get update
RUN apt-get install -y ffmpeg

# Cleanup.
RUN rm -rf /var/cache/* /tmp/*

WORKDIR /app

COPY . /app
COPY $VIDEO /app

ENTRYPOINT ["/app/entrypoint.sh"]

