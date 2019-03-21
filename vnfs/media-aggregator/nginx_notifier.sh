#!/bin/sh

while inotifywait -e modify /opt/nginx/nginx.conf; do /opt/nginx/sbin/nginx -s reload; done
#while inotifywait -e modify /var/lib/docker/volumes/my-vol/_data/nginx/nginx.cnof; do /var/lib/docker/volumes/my-vol/_data/nginx/sbin/nginx -s reload; done
