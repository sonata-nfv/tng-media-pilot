#!/bin/sh

source variables.env

echo "test"

mpv http://$STREAMING_ENGINE:80/hls/$STREAM.m3u8 --dump-stats=stats_test.txt --vo=null --ao=null --ao-null-untimed
#mpv http://192.168.137.72:8080/hls/demo1.m3u8


#ffplay -fflags nobuffer http://$STREAMING_ENGINE:8080/hls/$STREAM

