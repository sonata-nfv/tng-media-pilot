# Content producer emulator
The content producer emulator consists on a simple Docker container. 
This contains a video file and an instance of ffmpeg that plays that 
video. The ffmpeg does not transcodes the video, just sends it to the 
media-aggregator via RTMP, like if it was a camera. There are two separate
container tags, 360 which streams a 360 video and the plane tag that streams 
a secondary plane video. 

```docker run -d -e AGGREGATOR='[media-aggregator-ip]' -e APP='[nginx-app-route]' -e STREAM='[video-name]' ignaciodomin/media-cpe:[tag(360/plane)]```

#### CPE input parameters
* ```AGGREGATOR```: Here should be the IP of the target media-aggregator.
* ```APP```: This is the name of the camera, will be the application name 
in Nginx. The camera will send the video to this endpoint.
* ```STREAM```: This is the name of the video. This identifier will be the 
same in the player.  

## Stats from CPE
