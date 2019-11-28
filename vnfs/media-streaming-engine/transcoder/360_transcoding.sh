#!/bin/sh

/usr/local/bin/ffmpeg -i rtmp://localhost:1935/$1/$2 -r 30 \
    -filter_complex "[v:0]scale=1280:trunc(ow/a/2)*2[vout001]" \
    -c:v libx264 -preset veryfast -g 60 -sc_threshold 0 \
    -map [vout001] -c:v:0 libx264 -b:v:0 3000k \
    -map a:0 -c:a:0 aac -b:a:0 128k -ac 2 \
    -f hls -hls_time 6 -master_pl_name $2.m3u8 -hls_flags delete_segments \
    -var_stream_map "v:0,a:0" /opt/data/hls/$2_%v.m3u8 \
    2> /opt/data/logs/$2.txt