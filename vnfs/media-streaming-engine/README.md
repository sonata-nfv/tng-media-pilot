# media-streaming-engine

This VNF implements the adaptive streaming algorithm, first transcodes 
the video to different qualities and then generates the HLS manifest and video fragments. 

It is built with Nginx compiled with the RTMP module. The transcoding 
is implemented with ffmpeg.
```
ffmpeg -i rtmp://localhost:1935/$app/$name -async 1 -vsync -1
       -c:v libx264 -c:a libfdk_aac -profile:a aac_he -b:v 400k -b:a 64k -vf "scale=720:trunc(ow/a/2)*2" -tune zerolatency -preset superfast -f flv rtmp://localhost:1935/show/$name_mid
       -c:v libx264 -c:a libfdk_aac -profile:a aac_he -b:v 800k -b:a 64k -vf "scale=1280:trunc(ow/a/2)*2" -tune zerolatency -preset superfast -f flv rtmp://localhost:1935/show/$name_hd720
       -c:v copy -c:a libfdk_aac -profile:a aac_he -f flv rtmp://localhost:1935/show/$name_src; 
``` 

## Container details 
The media-streaming-engine is deployed on a docker container which contains an
Nginx server compiled with the RTMP-module and a Python script for the API. 
* Nginx + RTMP module: The main part of the container is an Nginx server
compiled with the RTMP-module. This module recieves the RTMP flows from the media-aggregator, 
then the input videos are transcoded to three different qualities with ffmpeg. After that, the MPEG-TS 
segments and the HLS playlist are generated. 
* ```media_aggregator_api.py```: This Python script contains the media-streaming-engine
API which serves the stats to the monitoring probe.

The container has two open ports for the different functions: 

| Port | function |
| --- | --- |
| `1935` | RTMP default port |
| `80` | HLS port|
| `5000` | API port |

## Qualities details
There are three different qualities configured in the streaming-engine:
* **Low:** 
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** 400k
    * **Audio bitrate:** 64k
    * **Resolution:** HD720
    * **Network bandwidth specification:** 4 Mbps
* **Mid:**
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** 800k
    * **Audio bitrate:** 64k
    * **Resolution:** HD1080
    * **Network bandwidth specification:** 8Mbps
* **Source:**
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** original
    * **Audio bitrate:** original 
    * **Resolution:** original
    * **Network bandwidth specification:** 10Mbps
