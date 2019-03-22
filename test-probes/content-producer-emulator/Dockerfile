FROM alfg/ffmpeg

ENV AGGREGATOR ""
ENV STREAM ""

ARG video
ENV VIDEO=$video

WORKDIR /app

COPY $VIDEO /app
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

