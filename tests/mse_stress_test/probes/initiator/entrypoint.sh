#!/bin/sh

source variables.env

#MEDIA SERVICE CONFIGURATION:

for camera in $CAMERAS
do
	#Register a camera:
	#It is possible to register multiple cameras, just put a curl per camera
	curl -H 'content-Type: application/json' -X POST -d '{"name":"'"$camera"'","type":"360"}' http://$CMS:50000/registerCamera

	#Connect a client: 
	#It is possible to connect multiple cameras, just put a curl per streaming-engine
	curl -H 'content-Type: application/json' -X GET -d '{"name":"'"$camera"'"}' http://$CMS:50000/getStreamURL
done
