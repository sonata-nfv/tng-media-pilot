#!/bin/sh

source variables.env

ffprobe -show_packets -select_streams v -print_format json hls+http://$STREAMING_ENGINE:80/hls/$STREAM.m3u8 > output.json



