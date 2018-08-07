#!/bin/sh

while inotifywait -e close_write /var/lib/docker/volumes/my-vol/_data/nginx/nginx.conf; do /var/lib/docker/volumes/my-vol/_data/nginx/nginx.conf -s reload; done
