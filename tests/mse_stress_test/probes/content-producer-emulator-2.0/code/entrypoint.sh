#!/bin/sh

mkdir -p /output/cpe/${HOSTNAME}

# Start the parser process:
/app/cpe.py &
status=$?
if [ $status -ne 1 ]; then 
    if [ $status -ne 0 ]; then
        echo "Failed to start cpe: $status"
        exit $status
    fi
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 1; do
    ps aux | grep cpe | grep -q -v grep
    PROCESS_1_STATUS=$?
    if [ $PROCESS_1_STATUS -ne 0 ]; then
        echo "One of the processes has already exited. ${PROCESS_1_STATUS}"
        exit 0
    fi
done