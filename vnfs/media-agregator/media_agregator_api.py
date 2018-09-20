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
import sqlite3 as lite

CONF_PATH = '/opt/nginx/nginx.conf'
#CONF_PATH = 'nginx.conf'

app = Flask(__name__)

"""This function creates an app in the nginx.conf for the new camera"""
@app.route("/connectCamera", methods=["PUT"])
def connect_camera():
    input_json = request.get_json()

    stream_app = input_json['stream_app']

    con = lite.connect('agregator.db')

    cur = con.cursor()
    cur.execute('INSERT INTO agregator (name) VALUES(?)', [stream_app])

    con.commit()

    cur.execute('SELECT * from agregator')
    table = cur.fetchall()
    table = sorted(table, key=lambda x: (x[0]))

    conf = open(CONF_PATH, 'r+')
    conf.seek(0)
    conf.write(render_template('nginx.conf', table=table))
    conf.truncate()
    conf.close()

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
    stream_engine_IP = input_json['stream_engine_IP']

    push_url = "push rtmp://"+stream_engine_IP+":1935/live/"+stream_key+";"

    con = lite.connect('agregator.db')

    cur = con.cursor()
    cur.execute('SELECT * from agregator')
    table = cur.fetchall()

    if stream_app in table:
        app_index = table.index(stream_app)
        if None in table[app_index]:
            del table[app_index]
            table.append(tuple((stream_app, push_url)))
            cur.execute('insert into agregator (name, url) values (?,?)', table[len(table)-1])
        else:
            table.append(tuple((stream_app, push_url)))
            cur.execute('insert into agregator (name, url) values (?,?)', table[len(table)-1])
    else:
        table.append(tuple((stream_app, push_url)))
        cur.execute('insert into agregator (name, url) values (?,?)', table[len(table)-1])

    con.commit()

    table = sorted(table, key=lambda x: (x[0]))

    conf = open(CONF_PATH, 'r+')
    conf.seek(0)
    conf.write(render_template('nginx.conf', table=table, table1=table))
    conf.truncate()
    conf.close()

    response = {}
    response["code"] = 200
    response["type"] = "?"
    response["message"] = "http://"+stream_engine_IP+":8080/hls/"+stream_key+".m3u8"

    return json.dumps(response, sort_keys= False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
