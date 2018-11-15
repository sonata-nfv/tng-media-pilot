# media-aggregator


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



    
