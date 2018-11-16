# tng-media-pilot service-test
The immersive media pilot will is tested with some emulators....
## Content Producer Emulator (CPE)
The content producer emulator consists on a simple Docker container. This
contains a video file and an instance of ffmpeg that plays that video. The 
ffmpeg does not transcodes the video, just sends it to the media-aggregator
via RTMP, like if it was a camera. 

The container starts with the following instruction:
```docker run -d -e AGGREGATOR='[media-aggregator-ip]' -e APP='[nginx-app-route]' -e STREAM='[video-name]' ignaciodomin/media-cpe:demo```
### Stats from CPE

## Content Consumer Emulator (CCE)


### Stats from CCE
    
