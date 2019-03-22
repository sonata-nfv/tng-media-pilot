FROM jwater7/mpv

ENV STREAMING_ENGINE ""
ENV STREAM ""
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

