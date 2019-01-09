#!/usr/bin/env bash

PAYLOAD="{"Aggregators":[{"name": "Aggregator-001","location": "Madrid","ip": "192.168.137.150:5000"},{"name":
"Aggregator-002","location": "Madrid","ip": "192.168.2.1:3450"}],"StreamingEngines":[{"name": "Engine-001","location":
"Madrid","ip": "192.168.137.151:1935"}]}"

curl -H'content-Type:application/json' -X POST -d'$PAYLOAD' http://192.168.137.150:50000/configure

