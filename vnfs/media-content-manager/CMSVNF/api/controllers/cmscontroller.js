'use strict'

let kAggregatorIP = process.env.AggregatorIP;

let kRequest = require('request');

function kAggregator( id, name, location, ip)
{
    this.id = id;

    this.name = name;

    this.location = location;

    this.ip = ip;
}

function kCamera( name)
{
    this.name = name;
}

function kStream( id, name, description, Aggregator_id)
{
    this.id = id;

    this.name = name;

    this.description = description;

    this.Aggregator_id = Aggregator_id;
}

let kAggregators = [];

let kCameras = [];

let kStreams = [];

// --- RegisterAggregator ------------------------------------------------------

exports.RegisterAggregator = function( req, res)
{
  console.log( req.body);

  res.status( 200);

  let kCheckValuesString = CheckValues( req.body, "id", "name", "location");

  if (kCheckValuesString != "")
  {
    res.status( 400);

    res.send( kCheckValuesString);
    
    return;
  }
  
  let kDuplicates = kAggregators.filter( function( object)
  {
    return object.id == req.body.id;
  });

  if (kDuplicates.length > 0 )
  {
    res.status( 409);

    res.send( "Aggregator already registered!");
    
    return;
  }

  res.json( "Aggregator registered successfully");

  let AggregatorIP = req.headers['x-forwarded-for'] ||
                     req.connection.remoteAddress;

  let kNewAggregator = new kAggregator( req.body.id,
                                        req.body.name,
                                        req.body.location,
                                        AggregatorIP
                                      );

  kAggregators.push( kNewAggregator);

  console.log( kAggregators);
};

// --- RegisterStream ----------------------------------------------------------

exports.RegisterStream = function( req, res)
{
  console.log( req.body);

  res.status( 200);

  let kCheckValuesString = CheckValues( req.body,
                                        "id",
                                        "name",
                                        "Aggregator_id");

  if (kCheckValuesString != "")
  {
    res.status( 400);

    res.send( kCheckValuesString);
    
    return;
  }
  
  let kAggregatorDuplicates = kAggregators.filter( function( object)
  {
    return object.id == req.body.Aggregator_id;
  });

  if ( kAggregatorDuplicates.length != 1)
  {
    res.status( 404);

    res.send( "Aggregator with id '" + req.body.Aggregator_id + "' not found!");

    return;
  }

  let kDuplicates = kStreams.filter( function( object)
  {
    return object.id == req.body.id;
  });

  if ( kDuplicates.length > 0)
  {
    res.status( 400);

    res.send( "Stream with id '" + req.body.id + "' already registered!");

    return;
  }

  res.json( "Stream registered successfully");

  let kDescription = ( req.body.hasOwnProperty( "description")) ?
                       req.body.description :
                       "";

  let kNewStream = new kStream( req.body.id,
                                req.body.name,
                                kDescription,
                                req.body.Aggregator_id);

  kStreams.push( kNewStream);

  console.log( kStreams);
};

// --- DisconnectStream --------------------------------------------------------

exports.DisconnectStream = function( req, res)
{
  console.log( req.body);

  res.status( 200);

  let kCheckValuesString = CheckValues( req.body,
                                        "stream_id",
                                        "Aggregator_id");

  if (kCheckValuesString != "")
  {
    res.status( 400);

    res.send( kCheckValuesString);
    
    return;
  }
  
  let kAggregatorDuplicates = kAggregators.filter( function( object)
  {
    return object.id == req.body.Aggregator_id;
  });

  if ( kAggregatorDuplicates.length != 1)
  {
    res.status( 404);

    res.send( "Aggregator with id '" + req.body.Aggregator_id + "' not found!");

    return;
  }

  let kDuplicates = kStreams.filter( function( object)
  {
    return object.id == req.body.stream_id;
  });

  if ( kDuplicates.length != 1)
  {
    res.status( 404);

    res.send( "Stream with id '" + req.body.stream_id + "' not found!");

    return;
  }

  res.json( "Stream removed successfully.");

  let iIndex = kStreams.indexOf(kDuplicates[0])

  kStreams.splice(iIndex, 1);

  console.log( kStreams);
};

// --- GetContentList ----------------------------------------------------------

exports.GetContentList = function( req, res)
{
  console.log( req.body);

  res.status( 200);

  res.send( kCameras);
};

// --- GetStreamURL ------------------------------------------------------------

exports.GetStreamURL = function( req, res)
{
  console.log(req.query);

  //todo: location check

  res.status( 200);

  let StreamURL = GetCameraStream(req.query.name);

  // hack for demo
  let UrlObject = {};

 /* if (req.query.stream_id === "Stream_1")
  {
    UrlObject.url = "https://www.nurogames.com/tmp-video/360_VR_Master_Series_Free_Download_Crystal_Shower_Falls.mp4";
  }
  else
  {
    UrlObject.url = "https://www.nurogames.com/tmp-video/TangoV2.mp4";
  }*/
  
  UrlObject.url = StreamURL;

  res.send(JSON.stringify(UrlObject));
  
  return;
  // hack end
  
  let kCheckValuesString = CheckValues( req.query,
                                        "stream_id");

  if (kCheckValuesString != "")
  {
    res.status( 400);

    res.send( kCheckValuesString);
    
    return;
  }

  let kStream = kStreams.filter( function( object)
  {
    return object.id == req.query.stream_id;
  });

  if (kStream.length == 0)
  {
    res.status( 404);

    res.send( "Stream with id '"+req.query.stream_id+"' not found.");

    return;
  }

  let kAggregator = kAggregators.filter( function( object)
  {
    return object.id == kStream[0].Aggregator_id;
  });

  if (kAggregator.length == 0)
  {
    res.status( 404);

    res.send( "No Aggregator is hosting this stream.");

    return;
  }

  kRequest( kAggregator[0].ip+"/connectStream?stream_id="+kStream[0].id,
            function ( error, response, body) {
              console.log("error: "+error);
              console.log('statusCode:', response && response.statusCode);
              res.send(body);
            });

};

// --- Register camera ---------------------------------------------------------

exports.RegisterCamera = function( req, res)
{
  console.log( req.body);

  res.status( 200);

  let kCheckValuesString = CheckValues( req.body, "name");

  if (kCheckValuesString != "")
  {
    res.status( 400);

    res.send( kCheckValuesString);
    
    return;
  }
  
  let kDuplicates = kCameras.filter( function( object)
  {
    return object.name == req.body.name;
  });

  if (kDuplicates.length > 0 )
  {
    res.status( 409);

    res.send( "Camera already registered!");
    
    return;
  }

  res.json( "Camera registered successfully");

  let kNewCamera = new kCamera( req.body.name);

  kCameras.push( kNewCamera);

  PostRegisterCamera( req.body);

  console.log( kCameras);
};


// --- Helper functions --------------------------------------------------------

function CheckValue( kTheObject, kTheValue)
{
  if ( kTheObject.hasOwnProperty(kTheValue) &&
       typeof kTheObject[kTheValue] === 'string' &&
       kTheObject[kTheValue].length)
  {
    return true;
  }
  else
  {
    return false;
  }
};

function CheckValues()
{
  if ( arguments.length < 2)
  {
    return "Error: wrong number of arguments.";
  }

  let kErrorMsg = ""; 

  let kTheObject = arguments[0];

  for ( let iNumArguments = 1;
        iNumArguments < arguments.length;
        ++iNumArguments)
  {
    if ( !CheckValue( kTheObject, arguments[iNumArguments]))
    {
      kErrorMsg += arguments[iNumArguments] + " is missing.\n";
    }
  }

  return kErrorMsg;
};

function PostRegisterCamera(postData)
{
  var clientServerOptions = {
      uri: 'http://'+kAggregatorIP+'/registerCamera',
      body: JSON.stringify(postData),
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  }
  kRequest(clientServerOptions, function (error, response) {
      if (error != null)
        console.log(error);
      else
        console.log(response.body);
      return;
  });
}

function GetCameraStream(postData)
{
  var clientServerOptions = {
      uri: 'http://'+kAggregatorIP+'/getStream',
      body: JSON.stringify(postData),
      method: 'GET',
      headers: {
          'Content-Type': 'application/json'
      }
  }
  kRequest(clientServerOptions, function (error, response) {
    if (error != null)
      console.log(error);
    else
      console.log(response.body);
    return response.body.url;
  });
}
