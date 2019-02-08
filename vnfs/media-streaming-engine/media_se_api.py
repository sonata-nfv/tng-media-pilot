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

from flask import Flask, request, json, render_template

import http.client, xmltodict, os

app = Flask(__name__)


"""This function reads the Nginx statistics and parses them to json format"""
@app.route("/stats", methods=["GET"])
def stats():
    ip = "localhost"
    port = "80"
    path = "/static/stat.xsl"

    conn = http.client.HTTPConnection(ip, port)

    conn.request("GET", path)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    data = data.decode("utf-8")

    dic = xmltodict.parse(data)

    #data = "<rtmp><nginx_version>1.13.9</nginx_version><nginx_rtmp_version>1.1.4</nginx_rtmp_version><compiler>gcc 5.3.0 (Alpine 5.3.0) </compiler><built>Jan 28 2019 13:32:33</built><pid>31</pid><uptime>10127</uptime><naccepted>2</naccepted><bw_in>4396944</bw_in><bytes_in>4200348922</bytes_in><bw_out>4399488</bw_out><bytes_out>4203357710</bytes_out><server><application><name>360</name><live><stream><name>360</name><time>55644</time><bw_in>4393888</bw_in><bytes_in>27313047</bytes_in><bw_out>4393888</bw_out><bytes_out>27313047</bytes_out><bw_audio>140448</bw_audio><bw_video>4253440</bw_video><client><id>7</id><address>192.168.137.151/live/360</address><time>55644</time><flashver>ngx-local-relay</flashver><dropped>0</dropped><avsync>-15</avsync><timestamp>55263</timestamp><active/></client><client><id>6</id><address>10.32.0.1</address><time>55778</time><flashver>FMLE/3.0 (compatible; Lavf57.83</flashver><dropped>0</dropped><avsync>-15</avsync><timestamp>55263</timestamp><publishing/><active/></client><meta><video><width>2048</width><height>1024</height><frame_rate>25</frame_rate><codec>Sorenson-H263</codec></video><audio><codec>MP3</codec><channels>2</channels><sample_rate>44100</sample_rate></audio></meta><nclients>2</nclients><publishing/><active/></stream><nclients>2</nclients></live></application><application><name>plane</name><live><nclients>0</nclients></live></application></server></rtmp>"

    #dic = xmltodict.parse(data)

    o_dic = {}
    o_dic["container_id"] = os.getenv("HOSTNAME")
    o_dic["bw_in"] = dic['rtmp']['bw_in']
    o_dic["bw_out"] = dic['rtmp']['bw_out']

    #Check the number of input connections:
    input_conn = 0
    for app in dic['rtmp']['server']['application']:
            input_conn = input_conn+1

    o_dic["input_conn"] = input_conn

    return json.dumps(o_dic, sort_keys=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)