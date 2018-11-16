# Content consumer emulator
The content consumer emulator consists on a simple Docker container. 
The container runs an instance of MPV player. The player requests the HLS
manifest to the media-streaming-engine. This simulates the user rol in the service. 

```sudo docker run -it --restart=always --privileged -e STREAMING_ENGINE='[media-streaming-engine-ip]' -e STREAM='[video-name]' -v vol1:/app ignaciodomin/media-cce:test1```

#### CCE input parameters
* ```STREAMING_ENGINE```: Here should be the IP of the media-streaming-engine.
* ```STREAM```: This is the name of the video. 

## Stats from CCE