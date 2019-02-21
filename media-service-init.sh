#!/usr/bin/env bash

#Variables with the IPs of the aggregator, streaming engine and cms:
MA="10.0.2.241:5000"
MSE="10.0.2.242:1935"
CMS="10.0.2.240:50000"

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
curl -H 'content-Type: application/json' -X POST -d '{"name":"360"}' http://$CMS/registerCamera
curl -H 'content-Type: application/json' -X POST -d '{"name":"plane"}' http://$CMS/registerCamera

#Connect a client: 
#It is possible to connect multiple cameras, just put a curl per streaming-engine
curl -H 'content-Type: application/json' -X GET -d '{"name":"360"}' http://$CMS/getStreamURL
curl -H 'content-Type: application/json' -X GET -d '{"name":"plane"}' http://$CMS/getStreamURL
