#!/usr/bin/env bash

#Create the wifi access-point
create_ap w1p6s0 eno1 corewifi pacopaco --daemon

#Modify the iptables 
iptables -t nat -A POSTROUTING -s 192.168.136.0/24 -o eno1 -j MASQUERADE

#MEDIA SERVICE CONFIGURATION:
#Service init config API (emulates the FSM function) 
curl -H'content-Type:application/json' -X POST -d'{
    "Aggregators": [
        {
            "name": "Aggregator-001",
            "location": "Madrid",
            "ip": "192.168.137.150:5000"
        },
        {
            "name": "Aggregator-002",
            "location": "Madrid",
            "ip": "192.168.2.1:5000"
        }
    ],
    "StreamingEngines": [
        {
            "name": "Engine-001",
            "location": "Madrid",
            "ip": "192.168.137.152:1935"
        }
    ]
}' http://192.168.137.150:50000/configure

#Register a camera:
curl -H 'content-Type: application/json' -X POST -d '{"name":"cam1"}' http://192.168.137.152:50000/registerCamera

#Connect a client: 
curl -H 'content-Type: application/json' -X GET -d '{"name":"cam1"}' http://192.168.137.152:50000/getStreamURL
