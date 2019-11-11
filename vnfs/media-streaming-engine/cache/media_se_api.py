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

import http.client, xmltodict, os, logging, requests

app = Flask(__name__)


# """This function reads the Nginx statistics and parses them to json format"""
# @app.route("/stats", methods=["GET"])
# def stats():
#     dic = nginxStats()

#     o_dic = {}
#     o_dic["resource_id"] = os.getenv("container_name")
#     o_dic["bw_in"] = dic['rtmp']['bw_in']
#     o_dic["bw_out"] = dic['rtmp']['bw_out']

#     #Check the number of input connections:
#     input_conn = 0
#     if dic['rtmp'].get('server'):
#         for app in dic['rtmp']['server']['application']:
#             input_conn = input_conn+1

#         o_dic["input_conn"] = input_conn

#     return json.dumps(o_dic, sort_keys=False)


# """This function checks the availability of the VNF"""
# @app.route("/status", methods=["GET"])
# def status():
#     dic = nginxStats()

#     uptime = dic['rtmp']['uptime']

#     if int(uptime) > 0:
#         status = "ok"
#     else:
#         status = "down"

#     response = {}
#     response["resource_id"] = os.getenv("container_name")
#     response["status"] = status

#     return json.dumps(response, sort_keys=False)


# def nginxStats():
#     ip = "localhost"
#     port = "80"
#     path = "/static/stat.xsl"

#     conn = http.client.HTTPConnection(ip, port)

#     conn.request("GET", path)
#     response = conn.getresponse()
#     data = response.read()
#     conn.close()

#     data = data.decode("utf-8")

#     dic = xmltodict.parse(data)

#     return dic

def get_mse_ip():
    name = os.getenv('name')
    vendor = os.getenv('vendor')
    version = os.getenv('version')

    mse_ip = '{name}_{vendor}_{version}_hls_ip'.format(name=name, vendor=vendor, version=version)

    return mse_ip

def register():
    name = os.getenv('HOSTNAME')
    location = '-' #TODO: add here a location, maybe an env var from slice?.
    ip = get_mse_ip()

    conf = {}
    conf['streamingengines'] = {}

    conf['streamingengines']['name'] = name
    conf['streamingengines']['location'] = location
    conf['streamingengines']['ip'] = ip

    api_endpoint = 'http://{}:50000/configure'.format(os.getenv('vnf_cms_eu_5gtango_0_8_api_ip'))
    body = json.dumps(conf, sort_keys=False)

    r = requests.post(url=api_endpoint, data=body)

    logging.info('{status}, {reason}'.format(status=r.status_code, reason=r.reason))

if __name__ == '__main__':

    if "CMS_IP" in os.environ:
        register()

    app.run(host='0.0.0.0', debug=True)