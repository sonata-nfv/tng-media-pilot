#!/bin/sh

# Start the nginx process:
/opt/nginx/sbin/nginx &
#/var/lib/docker/volumes/my-vol/_data/nginx/sbin/nginx &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start nginx: $status"
  exit $status
fi

# Start the media_agregator_api process:
/app/media_aggregator_api.py &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start media_aggregator_api: $status"
  exit $status
fi

# Start the media_agregator_api process:
#/app/stats_extractor.py &
#status=$?
#if [ $status -ne 0 ]; then
#  echo "Failed to start stats_extractor: $status"
#  exit $status
#fi

#Start the nginx_notifier process:
/app/nginx_notifier.sh &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start nginx_notifier: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  ps aux |grep nginx |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep media_aggregator_api.py |grep -q -v grep
  PROCESS_2_STATUS=$?
  #ps aux |grep stats_extractor.py |grep -q -v grep
  #PROCESS_3_STATUS=$?
  ps aux |grep nginx_notifier.sh |grep -q -v grep 
  PROCESS_3_STATUS=$?
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 -o $PROCESS_3_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
