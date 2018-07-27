'use strict'

function kAggregator( id, name, location)
{
    this.id = id;

    this.name = name;

    this.location = location;
}

function kStream( id, name, description, Aggregator_id)
{
    this.id = id;

    this.name = name;

    this.description = description;

    this.Aggregator_id = Aggregator_id;
}

let kAggregators = [];

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

  let kNewAggregator = new kAggregator( req.body.id,
                                        req.body.name,
                                        req.body.location);

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

  res.send( kStreams);
};

// --- GetStreamURL ------------------------------------------------------------

exports.GetStreamURL = function( req, res)
{
  console.log(req);

  console.log(res);
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
