#!/bin/sh

while inotifywait -e close_write /opt/nginx/nginx.conf; do /opt/nginx/sbin/nginx -s reload; done
