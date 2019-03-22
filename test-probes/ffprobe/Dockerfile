FROM sjourdan/ffprobe:latest

ENV STREAMING_ENGINE ""
ENV STREAM ""

WORKDIR /app
COPY . /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
