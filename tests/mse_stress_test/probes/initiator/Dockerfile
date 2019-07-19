FROM alpine:3.4

ENV CMS ""
ENV CAMERAS ""

RUN apk add --update \
    curl \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app 

ENTRYPOINT ["/app/entrypoint.sh"]
