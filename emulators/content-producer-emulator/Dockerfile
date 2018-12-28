FROM ubuntu:trusty

ENV AGGREGATOR ""
ENV APP ""
ENV STREAM ""

RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:mc3man/trusty-media -y
RUN apt-get update
RUN apt-get install -y ffmpeg

# Cleanup.
RUN rm -rf /var/cache/* /tmp/*

WORKDIR /app

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

