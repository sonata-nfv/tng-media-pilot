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
## acknowled10.200.16.11ge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).

import json
import logging
import os
import threading
import time

import requests


def send_video(video, aggregator, stream):
    try:
        logging.info('{}, {}, {}'.format(video, aggregator, stream))
        os.system("ffmpeg -hide_banner -loglevel panic -stream_loop -1 -re -i /app/video/{} -f flv rtmp://{}:1935/{}/{}".format(video, aggregator, stream, stream))
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    counter = 0
    logs = {}

    #cms = os.getenv('CMS')
    aggregator = os.getenv('AGGREGATOR')
    mse = os.getenv('STREAMINGENGINE')
    video = os.getenv('VIDEO')

    processes = []

    while counter < 6:
        stream = 'test{}'.format(counter)
        
        #Register the camera in the CMS:
        api_endpoint = 'http://{}:5000/registerCamera'.format(aggregator)

        json_body = {}
        json_body['name'] = stream
        json_body['type'] = '360'
        
        body = json.dumps(json_body, sort_keys=False)
        logging.info('Body: {}'.format(body))

        try:
            r = requests.post(url=api_endpoint, data=body, headers={'Content-type': 'application/json'})
        except requests.exceptions.RequestException as e:
            logging.error('{}'.format(e))

        logging.info('{}, {}'.format(r.status_code, r.reason))

        #Connect the MA with the MSE:
        api_endpoint = 'http://{}:5000/getStream'.format(aggregator)

        json_body = {}
        json_body['name'] = stream
        json_body['se_ip'] = mse

        body = json.dumps(json_body, sort_keys=False)
        logging.info('Body: {}'.format(body))

        try:
            r = requests.get(url=api_endpoint, data=body, headers={'Content-type': 'application/json'})
        except requests.exceptions.RequestException as e:
            logging.error('{}'.format(e))

        logging.info('{}, {}'.format(r.status_code, r.reason))

        #Start the FFmpeg script:
        logging.info('Executing script {}'.format(counter)) 
        time.sleep(2)
        ffmpeg_process = threading.Thread(target=send_video, args=[video, aggregator, stream])
        processes.append(ffmpeg_process)
        ffmpeg_process.start()
        logging.info('FFMPEG process {} started'.format(counter))
        #subprocess.Popen(['/app/send-video.sh', video, aggregator, stream])

        logging.info('Waiting 2 minutes...')
        #Sleep 2 minutes: 
        counter = counter + 1
        time.sleep(600)

    logging.info('All the FFMPEG process were executed')

    for process in processes:
        process._stop()

    if counter is 6:
        logs['completed'] = 'ok'
    else: 
        logs['completed'] = 'fail'

    with open('logs.txt', 'w') as fp:
        json.dump(logs, fp)

    exit(2)