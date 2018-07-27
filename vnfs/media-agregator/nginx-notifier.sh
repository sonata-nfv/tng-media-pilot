#!/bin/sh

if inotifywait -t 0 -m -e close_write /opt/nginx/nginx.conf; then
	/opt/nginx/sbin/nginx -s reload
fi
