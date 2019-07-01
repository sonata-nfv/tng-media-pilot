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

import json, sys, os

def parse_logs(path):

    with open(path) as json_file:
        data = json.load(json_file)

    framesRecieved = len(data['frames'])
    framesTotal = 1800 #1min video * 30fps
    framesLost = framesTotal - framesRecieved

    return framesLost


if __name__ == '__main__':

    rootdir = '/output'
    writePath = '/output/parser' + os.getenv("HOSTNAME")
    logs = 'logs.txt'

    framesLost = []

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file == 'logs.txt':
                path = os.path.join(rootdir, file)
                framesLost.insert(file.index(), parse_logs(path))

    framesLostTotal = 0

    for frame in range(0, len(framesLost)):
        framesLostTotal = framesLostTotal + frame

    result = {}
    result['frames-lost'] = framesLostTotal

    with open(writePath+'/result.json', 'w') as results:
         json.dump(result, results)

    sys.exit()
