#!/usr/bin/env bash

#Create the wifi access-point
#create_ap w1p6s0 eno1 corewifi pacopaco --daemon

#Modify the iptables
#iptables -t nat -A POSTROUTING -s 192.168.136.0/24 -o eno1 -j MASQUERADE

#Variables with the IPs of the aggregator, streaming engine and cms:
MA="172.31.13.44:5000"
MSE="172.31.13.46:1935"
CMS="172.31.13.45:50000"

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
curl -H 'content-Type: application/json' -X POST -d '{"name":"plane"}' http://$CMS/registerCamera

#Register a camera:
curl -H 'content-Type: application/json' -X POST -d '{"name":"360"}' http://$CMS/registerCamera



#Connect a client: 
curl -H 'content-Type: application/json' -X GET -d '{"name":"plane"}' http://$CMS/getStreamURL

#Connect a client: 
curl -H 'content-Type: application/json' -X GET -d '{"name":"360"}' http://$CMS/getStreamURL
