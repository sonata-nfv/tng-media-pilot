FROM jwater7/mpv

ENV STREAMING_ENGINE ""
ENV STREAM ""
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \ 
  && apt-get install -y ffmpeg \
  && apt-get install -y curl 

RUN curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

WORKDIR /app

COPY . /app

ENTRYPOINT [ "/app/entrypoint.sh" ]

