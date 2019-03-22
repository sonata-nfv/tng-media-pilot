#!/bin/sh

source variables.env

#Start the ffmpeg process:
ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/$VIDEO -f flv rtmp://$AGGREGATOR:1935/$STREAM/$STREAM > /output/cpe/logs.txt


