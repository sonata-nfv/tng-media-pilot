"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import logging
import os
import yaml
import json
import requests
import time
import configparser
from sonsmbase.smbase import sonSMbase
from .ssh import Client
import netaddr


def reverse(ip):
        if len(ip) <= 1:
                return ip
        l = ip.split('.')
        return '.'.join(l[::-1])

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("fsm-start-stop-configure")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class CssFSM(sonSMbase):
    
    hostIp = 'none'
    def __init__(self):

        """
        :param specific_manager_type: specifies the type of specific manager
        that could be either fsm or ssm.
        :param service_name: the name of the service that this specific manager
        belongs to.
        :param function_name: the name of the function that this specific
        manager belongs to, will be null in SSM case
        :param specific_manager_name: the actual name of specific manager
        (e.g., scaling, placement)
        :param id_number: the specific manager id number which is used to
        distinguish between multiple SSM/FSM that are created for the same
        objective (e.g., scaling with algorithm 1 and 2)
        :param version: version
        :param description: description
        """

        self.specific_manager_type = 'fsm'
        self.service_name = 'cms'
        self.function_name = 'cms'
        self.specific_manager_name = 'css'
        self.num_lb = 0
        self.old_ips = []
        self.id_number = '1'
        self.version = 'v0.1'
        self.description = "An FSM that configures the CMS with the MAs and MSEs deployed."

        super(self.__class__, self).__init__(specific_manager_type=self.specific_manager_type,
                                             service_name=self.service_name,
                                             function_name=self.function_name,
                                             specific_manager_name=self.specific_manager_name,
                                             id_number=self.id_number,
                                             version=self.version,
                                             description=self.description)

    def on_registration_ok(self):

        # The fsm registration was successful
        LOG.debug("Received registration ok event, FSM is running.")

        # send the status to the SMR
        status = 'Subscribed, waiting for alert message'
        message = {'name': self.specific_manager_id,
                   'status': status}
        self.manoconn.publish(topic='specific.manager.registry.ssm.status',
                              message=yaml.dump(message))

        # Subscribing to the topics that the fsm needs to listen on
        topic = "generic.fsm." + str(self.sfuuid)
        self.manoconn.subscribe(self.message_received, topic)
        LOG.info("Subscribed to " + topic + " topic.")

    def message_received(self, ch, method, props, payload):
        """
        This method handles received messages
        """

        # Decode the content of the message
        request = yaml.load(payload)

        # Don't trigger on non-request messages
        if "fsm_type" not in request.keys():
            LOG.info("Received a non-request message, ignoring...")
            return

        # Create the response
        response = None

        # the 'fsm_type' field in the content indicates for which type of
        # fsm this message is intended. In this case, this FSM functions as
        # start, stop and configure FSM
        if str(request["fsm_type"]) == "start":
            LOG.info("Start event received: " + str(request["content"]))
            response = self.start_event(request["content"])

        if str(request["fsm_type"]) == "configure":
            LOG.info("Config event received: " + str(request["content"]))
            response = self.configure_event(request["content"])

        # If a response message was generated, send it back to the FLM
        if response is not None:
            # Generated response for the FLM
            LOG.info("Response to request generated:" + str(response))
            topic = "generic.fsm." + str(self.sfuuid)
            corr_id = props.correlation_id
            self.manoconn.notify(topic,
                                 yaml.dump(response),
                                 correlation_id=corr_id)
            return

        # If response is None:
        LOG.info("Request received for other type of FSM, ignoring...")

    def start_event(self, content):
        """
        This method handles a start event.
        """

        self.vnfr = content['vnfr']
        self.mgmt_ip = content['vnfr']['virtual_deployment_units'][0]['vnfc_instance'][0]['connection_points'][0]['interface']['address']
        LOG.info('mgmt_ip: ' + str(self.mgmt_ip))

        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'

        return response

    def configure_event(self, content):
        """
        This method handles a configure event.
        """

        # The config event receives a list if IP addresses of backends. The
        # load needs to be balanced among these IP addresses.
        LOG.info(str(content))

        # TODO: Parse the yaml and create the json payload for the CMS

        payload = {}
        payload['name'] = 'squid'
        payload['port'] = 80
        payload['backends'] = []

        counter = 1
        for backend in content['ips']:
            new_backend = {}
            new_backend['name'] = 'vnf' + str(counter)
            new_backend['host'] = backend
            new_backend['port'] = 3128
            payload['backends'].append(new_backend)
            counter = counter + 1

        wrapper = []
        wrapper.append(payload)

        LOG.info('message for haproxy: ' + str(wrapper))
        LOG.info(json.dumps(wrapper))

        header = {'Content-Type': 'application/json'}
        url = 'http://' + content['mgmt_ip'] + ':5000/'

        i = 1
        while i < 25:
            try:
                post = requests.post(url,
                                     data=json.dumps(wrapper),
                                     headers=header,
                                     timeout=5.0)
                LOG.info(str(post.status_code))
                LOG.info(str(post.text))
                break
            except:
                LOG.info("Retry, current attempt: " + str(i))
                i = i + 1
                time.sleep(10)

        response = {}
        response['status'] = 'COMPLETED'
        LOG.info("Response message: " + str(response))
        return response


def main():
    CssFSM()

if __name__ == '__main__':
    main()
