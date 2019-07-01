#!/bin/sh

source variables.env

#mkdir -p /output/cpe/${HOSTNAME}

# Start the ffmpeg process:
ffmpeg -fflags +genpts -f lavfi -i testsrc=duration=80:size=1920x1080:rate=30 -f flv rtmp://$AGGREGATOR:1935/$STREAM/$STREAM &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start ffmpeg: $status"
  exit $status
fi

# Start the ffprobe process:
#ffprobe -show_frames -select_streams v -print_format json -i "rtmp://${AGGREGATOR}:1935/${STREAM}/${STREAM}" > /output/cpe/${HOSTNAME}/logs.txt &
#status=$?
#if [ $status -ne 0 ]; then
#  echo "Failed to start ffprobe: $status"
#  exit $status
#fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 1; do
  ps aux |grep ffmpeg |grep -q -v grep
  PROCESS_1_STATUS=$?
#  ps aux |grep ffprobe |grep -q -v grep
#  PROCESS_2_STATUS=$?
  if [ $PROCESS_1_STATUS -ne 0 ]; then
    echo "One of the processes has already ended."
    exit 0
  fi
done
