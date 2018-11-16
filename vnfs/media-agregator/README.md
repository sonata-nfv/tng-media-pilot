# media-aggregator
## General description
The media-aggregator is the component that receives the video streams 
from the cameras, and also, redirects that videos to the different 
media-streaming-engines or to other media-aggregator in another network 
node when needed.

## Container details 
The media-aggregator is deployed on a docker container which contains an
Nginx server compiled with the RTMP-module, some Python scripts for the API
and stats extraction and also a simple inotifier script. 
* Nginx + RTMP module: The main part of the container is an Nginx server
compiled with the RTMP-module. This module manages RTMP video streams. 
* Pythons scripts: 
    * ```media_aggregator_api.py```: This Python script contains the media-aggregator
    API which communicates with the media-content-manager.
    * ```stats_extractor.py```: This script retrieves some stats from Nginx.
* ```nginx_notifier.sh```: this script is watching for changes in nginx.conf, when 
there are changes, the script reloads the configuration of Nginx 
without stopping the service.

## Nginx configuration
The most important part of the configuration file is the rtmp server part. 
When the media-content-manager registers a new camera, the API python code
creates a new application for that camera thanks to a Jinja template of
the Nginx configuration file. If a user request a video, the media-content-manager
asks for the media-aggregator to create a new RTMP push. This instruction 
will redirect the video from one camera (application) to a media-streaming-engine
or to another media-aggregator in another node depending on user's location. 

Here is an example of the rtmp server block inside ```nginx.conf``` with two cameras connected 
and serving video to three different media-streaming-engines:
```
rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application example1 {
            live on;
            record off;
            
            push rtmp://1.1.1.1:1935/live/example1;
            push rtmp://2.2.2.2:1935/live/example1;
        }
        
        application example2 {
            live on;
            record off;
            
            push rtmp://3.3.3.3:1935/live/example2;
        }
    }
}
```

## API description
### connectCamera
This method creates a new application inside Nginx where the camera can send the video through RTMP. The input of this method is a simple JSON file:

    {
		"stream_app": "name_of_the_app"
	}

The API will add the application into the nginx.conf file and reloads that configuration automatically without stop the service. 

The response will be the following: ????

Here is an example call for this method:

    curl -H 'content-Type: application/json' -X PUT -d '{"stream_app":"name_of_the_app"}' http://[IP_of_the_aggregator]:5000/connectCamera

### connectStream
This method will add a push order in the nginx configuration file. This push order will redirect the input flow of an specific application to the streaming-engine which corresponds. This is the JSON input:

    {
		"stream_key": "name_of_the_stream",
		"stream_app": "name_of_the_app",
		"stream_engine_IP": "IP_of_the_SE"
	}
    
The response will be the following: ????

Here is an example call:

    curl -H 'content-Type: application/json' -X PUT -d '{"stream_key":"name_of_the_stream","stream_app":"name_of_the_app","stream_engine_IP":"IP_of_the_SE"}' http://[IP_of_the_aggregator]:5000/connectCamera



    

    
