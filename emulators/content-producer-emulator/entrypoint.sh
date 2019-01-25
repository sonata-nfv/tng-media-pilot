#!/bin/sh

source variables.env

#FFREPORT=file=ffreport.log:repeat+verbose ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/video1.mkv -vcodec libx264 -x264-params keyint=2:scenecut=0 -acodec copy -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM
#ffmpeg -i /app/video1.mkv -deinterlace -c:v libx264 -pix_fmt yuv420p -s 1920x1080 -preset superfast -vb 6000k -r 30 -g 60 -bufsize 8000k -c:a aac -b:a 128k -ar 44100 -ac 2 -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM
#FFREPORT=file=ffreport.log:repeat+verbose ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/video1.mkv -deinterlace -vcodec libx264 -pix_fmt yuv420p -preset medium -r 30 -g 60 -b:v 6000k -acodec libmp3lame -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM
#FFREPORT=file=ffreport.log:repeat+verbose ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/video1.mkv -c:v copy -c:a copy -g 60 -f flv rtmp://$AGGREGATOR:1935/live/$APP/$STREAM
ffmpeg -loglevel repeat+verbose -stream_loop -1 -re -i /app/$VIDEO -f flv rtmp://$AGGREGATOR:1935/$APP/$STREAM
