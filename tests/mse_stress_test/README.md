<p align="center"><img src="https://github.com/sonata-nfv/tng-api-gtw/wiki/images/sonata-5gtango-logo-500px.png" /></p>

# MSE stress test

## Description
This test is designed to stress the CPU of the Media Streaming Engine CNF. This CNF does the transcoding of the videos to the different qualities, which is the 
the task that more computing power needs. 

The easiest way to stress this component of the service is putting different videos on the input of the CNF. Something that 
needs to be clarified is that the number of clients of these videos doesn't affect too much to the CPU, because the transcoding only depends 
on the number and type of inputs, not of the outputs.

## Components
The test is composed of the Immersive Media Network Service (without the Twitter CNF) deployed in Kubernetes and some test probes:
* Initiator: This probes configures the cameras and all the necessary stuff needed to run the service for this test.
* Content Producer Emulator (CPE): This probe simulates a 360 video RTMP flow. 
* Parser: Reads the logs from the probes and generates a result in json format.


