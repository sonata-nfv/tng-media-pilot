# -*- coding: utf-8 -*-

#!/usr/bin/python3

## Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).

import http.client, xmltodict, json, socket

ip="localhost"
port="8080"
path="/static/stat.xsl"

conn = http.client.HTTPConnection(ip,port)

conn.request("GET",path)
response = conn.getresponse()
data = response.read()
conn.close()

data = data.decode("utf-8")

dic = xmltodict.parse(data)

json_string = json.dumps(dic)
#with open('/opt/stats/MA_stats.json','w') as statsfile:
#    json.dumps(dic, statsfile)

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/opt/stats/MA_stats.json") #TODO: change to json file
s.send(json_string) #TODO: send json file encoded to bytes
#data = s.recv(1024)
#print('Received ' + repr(data))
#s.send(b'Hello, world 2\nOtra linea')
#data = s.recv(1024)
s.close()
#print('Received ' + repr(data))