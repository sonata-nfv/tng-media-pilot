#!/bin/sh

source variables.env

ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/$VIDEO -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM
