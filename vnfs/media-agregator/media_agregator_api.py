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

import conf_formatter
from flask import Flask, request, json

CONF_PATH = '/var/lib/docker/volumes/my-vol/_data/nginx/nginx.conf'
#CONF_PATH = 'nginx.conf'

app = Flask(__name__)

"""This function creates an app in the nginx.conf for the new camera"""
@app.route("/connectCamera", methods=["PUT"])
def connect_camera():
    input_json = request.get_json()

    stream_app = input_json['stream_app']

    code_block = "application "+ stream_app + " {\n " \
                                              "live on;\n " \
                                              "record off;\n" \
                                              "#-Insert Push here-\n" \
                                              "}\n"

    with open(CONF_PATH, "r") as myfile:
        data = myfile.readlines()
        index = data.index('        #-Insert Application here-\n')
        data.insert(index + 1, code_block)

        data_str = ''.join(data)

        with open(CONF_PATH, "w") as output:
            output.write(data_str)

    conf_formatter.format_config_file("CONF_PATH")

    response = {}
    response["code"] = 200
    response["type"] = "?"
    response["message"] = "TODO"

    return json.dumps(response, sort_keys=False)


"""This function adds a push statement in the specific app"""
@app.route("/connectStream", methods=["PUT"])
def connect_stream():
    input_json = request.get_json()

    stream_app = input_json['stream_app']
    stream_key = input_json['stream_key']

    push_url = "push rtmp://10.100.16.56:1935/stream/"+stream_key+";" #TODO: Change the harcoded url to the real server

    with open(CONF_PATH, "r") as myfile:
        data = myfile.readlines()
        index = data.index('        application ' + stream_app + ' {\n')
        data.insert(index + 4, push_url)

        data_str = ''.join(data)

        with open(CONF_PATH, "w") as output:
            output.write(data_str)

    conf_formatter.format_config_file(CONF_PATH)

    response = {}
    response["code"] = 200
    response["type"] = "?"
    response["message"] = "http://10.100.16.56/live/"+stream_key+".m3u8" #TODO: Change the harcoded url to the real server

    return json.dumps(response, sort_keys= False)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
