#!/usr/bin/python

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

import json, sys, os, m3u8, wget

variants = [os.getenv('STREAM') + '_0', os.getenv('STREAM') + '_1']

def readVariants():
    for variant in variants:
        uri = 'http://' + os.getenv('STREAMING_ENGINE') + ':80/hls/' + variant + '.m3u8'
        savePath = 'output/playlist_reader/' + os.getenv('HOSTNAME') + '/' + variant + '.m3u8'

        wget.download(variant, variant)

    generateLogs()

def generateLogs():
    logs = {}
    logs['variants'] = {}

    index = 0
    for variant in variants:
        with open(variant + '.m3u8', 'r') as content:
            content = content.read()
            m3u8_obj = m3u8.parser.parse(content)
            logs['variants'][index] = {}
            logs['variants'][index]['targetduration'] = m3u8_obj['targetduration']
            logs['variants'][index]['segments'] = {}
            index2 = 0
            for segment in m3u8_obj['segments']:
                logs['variants'][index]['segments'][index2] = segment['duration']
                index2 = index2+1
            index = index+1

    with open('logs.txt', 'w') as fp:
        json.dump(logs, fp)


if __name__ == '__main__':

    readVariants()

    sys.exit(0)
