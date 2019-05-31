#!/bin/sh

source variables.env

#MEDIA SERVICE CONFIGURATION:

#Register a camera:
#It is possible to register multiple cameras, just put a curl per camera
curl -H 'content-Type: application/json' -X POST -d '{"name":"'"$CAMERA"'","type":"plane"}' http://$CMS:50000/registerCamera

#Connect a client: 
#It is possible to connect multiple cameras, just put a curl per streaming-engine
curl -H 'content-Type: application/json' -X GET -d '{"name":"'"$CAMERA"'"}' http://$CMS:50000/getStreamURL

exit_status = $?
if [ $exit_status != 0 ]
  then
    exit $exit_status
fi

