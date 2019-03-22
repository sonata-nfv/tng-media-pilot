#!/bin/sh

source variables.env

ffprobe -show_packets -select_streams v -print_format json rtmp://$STREAMING_ENGINE:1935/live/$STREAM > /output/ffprobe/logs.txt | grep -n K_ -B 10
