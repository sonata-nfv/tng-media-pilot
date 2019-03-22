#!/bin/sh

source variables.env

#Start the MPV process:
mpv http://$STREAMING_ENGINE:80/hls/$STREAM.m3u8 --dump-stats=/app/stats_test.txt --vo=null --ao=null --ao-null-untimed

