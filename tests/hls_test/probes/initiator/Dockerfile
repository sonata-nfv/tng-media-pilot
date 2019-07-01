FROM alpine:3.4

ENV CMS ""
ENV CAMERA ""

RUN apk add --update \
    curl \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . /app 

ENTRYPOINT ["/app/entrypoint.sh"]
