#!/usr/bin/env bash

#Variables with the IPs of the aggregator, streaming engine and cms:
MA="IP:5000"
MSE="IP:1935"
CMS="IP:50000"

#MEDIA SERVICE CONFIGURATION:
#Service init config API (emulates the FSM function)
curl -H'content-Type:application/json' -X POST -d'{
    "Aggregators": [
        {
            "name": "Aggregator-001",
            "location": "Madrid",
            "ip": "'"$MA"'"
        }
    ],
    "StreamingEngines": [
        {
            "name": "Engine-001",
            "location": "Madrid",
            "ip": "'"$MSE"'"
    	}
    ]

}' http://$CMS/configure


#Register a camera:
#It is possible to register multiple cameras, just put a curl per camera
#curl -H 'content-Type: application/json' -X POST -d '{"name":"cam_name"}' http://$CMS/registerCamera


#Connect a client: 
#It is possible to connect multiple cameras, just put a curl per streaming-engine
#curl -H 'content-Type: application/json' -X GET -d '{"name":"cam_name"}' http://$CMS/getStreamURL
