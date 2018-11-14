#!/bin/sh

source variables.env

FFREPORT=file=ffreport.log:repeat+verbose ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/video1.mkv -c copy -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM > output.txt

