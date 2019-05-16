# media-streaming-engine

This VNF implements the adaptive streaming algorithm, first transcodes 
the video to different qualities and then generates the HLS playlist and the video fragments. 

It is built with Nginx compiled with the RTMP module. The transcoding 
is implemented with ffmpeg. The video transcoding is divided in two different applications, one for 360 videos and other one for plane videos. The plane videos are going to be shown on a little virtual screen, so it is enough with a 720p video resolution instead of a FullHD one and also without audio, this will save hardware resources. For the 360 videos, there are more variants with higher resolutions, up to 4K. 

Transcoding of a plane video:
```
ffmpeg -i rtmp://localhost:1935/$app/$name -filter_complex "[v:0]split=2[vtemp001][vtemp002];[vtemp001]scale=960:trunc(ow/a/2)*2[vout001];[vtemp002]scale=1280:trunc(ow/a/2)*2[vout002]"
            -c:v libx264 -preset veryfast -g 120 -sc_threshold 0 -map [vout001] -c:v:0 libx264 -b:v:0 2000k -map [vout002] -c:v:1 libx264 -b:v:1 6000k
            -an -f hls -hls_time 4 -master_pl_name $name.m3u8 -hls_flags independent_segments
            -var_stream_map "v:0 v:1" /opt/data/hls/$name_%v.m3u8; 
``` 

Transcoding of a 360 video:
```
ffmpeg -i rtmp://localhost:1935/$app/$name -filter_complex "[v:0]split=3[vtemp001][vtemp002][vout003];[vtemp001]scale=1280:trunc(ow/a/2)*2[vout001];[vtemp002]scale=1920:trunc(ow/a/2)*2[vout002]" -c:v libx264 -preset
            veryfast -g 120 -sc_threshold 0 -map [vout001] -c:v:0 libx264 -b:v:0 3000k -map [vout002] -c:v:1 libx264 -b:v:1 6000k -map [vout003] -c:v:2 libx264 -b:v:2 13000k
            -map a:0 -c:a:0 aac -b:a:0 128k -map a:0 -c:a:1 aac -b:a:1 196k -ac 2 -f hls -hls_time 4 -master_pl_name $name.m3u8 -hls_flags independent_segments
            -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:1" /opt/data/hls/$name_%v.m3u8;
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

The container has three open ports for the different functions: 

| Port | function |
| --- | --- |
| `1935` | RTMP default port |
| `80` | HLS port|
| `5000` | API port |

## Qualities details
For plane/secondary videos, we have two different qualities:
* **Low:** 
    * **Video codec:** H264
    * **Audio codec:** -
    * **Video bitrate:** 2000kbps
    * **Audio bitrate:** -
    * **Resolution:** 960x540 px
    * **Network bandwidth specification:** 20000kbps
* **High:**
    * **Video codec:** H264
    * **Audio codec:** -
    * **Video bitrate:** 6000kpbs 
    * **Audio bitrate:** -
    * **Resolution:** 1280x720 px
    * **Network bandwidth specification:** 6000kbps
    
For 360 videos, there are three different variants for the streaming
* **Low:** 
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** 3000kbps
    * **Audio bitrate:** 128kbps
    * **Resolution:** 1280x640 px
    * **Network bandwidth specification:** 3128kbps
* **Mid:**
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** 6000kpbs 
    * **Audio bitrate:** 128kbps
    * **Resolution:** 1920x960 px
    * **Network bandwidth specification:** 6128kbps
* **High:**
    * **Video codec:** H264
    * **Audio codec:** AAC
    * **Video bitrate:** 13000kpbs 
    * **Audio bitrate:** 196kbps
    * **Resolution:** Source 
    * **Network bandwidth specification:** 13196kbps

## API description
### stats
This method collects the stats from the Nginx server. It is called with:
        
    curl -H 'content-Type: application/json' -X GET [IP_of_the_mse]:5000/stats    

Here there is an example of the response:

    {
        "resource_id": "eu-5gtango-vnf-mse-0-4-fbf0a168-7dd5449879-bqd9s",
        "bw_in":"4396944",
        "bw_out":"4399488",
        "input_conn":2
    }

### status
This method tells to the CMS if the Nginx server is running correctly (`ok`) or not (`down`). It is called with:

    curl -H 'content-Type: application/json' -X GET [IP_of_the_mse]:5000/status
    
Here there is an example of the response:

    {
        "resource_id": "eu-5gtango-vnf-mse-0-4-fbf0a168-7dd5449879-bqd9s", 
        "status": "ok"
    }
