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

import http.client, xmltodict, os, uuid

CONF_PATH = '/opt/nginx/nginx.conf'

app = Flask(__name__)


"""This function creates an app in the nginx.conf for the new camera"""
@app.route("/registerCamera", methods=["POST"])
def register_camera():
    input_json = request.get_json()

    camera_name = input_json['name']

    with open("conf.json") as conf_json:
        data = json.load(conf_json)

    data["cameras"].append({
        "name": camera_name,
        "streamingEngines": []
    })

    with open("conf.json", "w") as conf_json:
        json.dump(data, conf_json)

    update_nginx(data)

    response = {}
    #response["uuid"] = str(uuid.uuid4())
    response["endpoint"] = "rtmp://10.100.32.240:1935/"+camera_name+"/"+camera_name #TODO: Put the correct MA IP

    return json.dumps(response, sort_keys=False)

"""This function adds a push statement in the specific app"""
@app.route("/getStream", methods=["GET"])
def get_stream():
    input_json = request.get_json()

    stream_app = input_json["name"]
    streaming_engine_IP = input_json["se_ip"]
    streaming_engine_IP = streaming_engine_IP.split(':')[0]

    with open("conf.json") as conf_json:
        data = json.load(conf_json)

    for camera in data['cameras']:
        if camera['name'] == stream_app:
            camera['streamingEngines'].append(streaming_engine_IP)

    with open("conf.json", "w") as conf_json:
        json.dump(data, conf_json)

    update_nginx(data)

    response = {}
    response["url"] = "http://"+streaming_engine_IP+":80/hls/"+stream_app+".m3u8"

    return json.dumps(response, sort_keys=False)

"""This function reads the Nginx statistics and parses them to json format"""
@app.route("/stats", methods=["GET"])
def stats():
    dic = nginxStats()

    o_dic = {}
    o_dic["resource_id"] = os.getenv("HOSTNAME")
    o_dic["bw_in"] = dic['rtmp']['bw_in']
    o_dic["bw_out"] = dic['rtmp']['bw_out']

    #Check the number of input connections:
    input_conn = 0
    if dic['rtmp'].get('server'):
        for app in dic['rtmp']['server'].get('application'):
            input_conn = input_conn+1

        o_dic["input_conn"] = input_conn

    return json.dumps(o_dic, sort_keys=False)

"""This function checks the availability of the VNF"""
@app.route("/status", methods=["GET"])
def status():
    dic = nginxStats()

    uptime = dic['rtmp']['uptime']

    if int(uptime) > 0:
        status = "ok"
    else:
        status = "down"

    response = {}
    response["resource_id"] = os.getenv("HOSTNAME")
    response["status"] = status

    return json.dumps(response, sort_keys=False)

def nginxStats():
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

    return dic

def update_nginx(data):
    conf = open(CONF_PATH, 'r+')
    conf.seek(0)
    conf.write(render_template('nginx.conf', data=data))
    conf.truncate()
    conf.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)