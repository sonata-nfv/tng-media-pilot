// ****************************************************************************
//
// Project: 5GTango
// Module: Twitterstream Virtual Network Function
//
// License:
//          
// Copyright 2018 Nurogames GmbH
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// ****************************************************************************

"use strict"

process.title = 'wsServerTest';

let kWebsocketServerPort = 50001;

let kWebSocketServer = require('websocket').server;
let kHttp = require('http');

var OAuth = require('oauth').OAuth
  , kOAuth = new OAuth(
    "https://api.twitter.com/oauth/request_token",
    "https://api.twitter.com/oauth/access_token",
    "Access",
    "Access",
    "1.0",
    "oob",
    "HMAC-SHA1"
  );

let kLoggedUsers = [];
let kClients = [];
let TwitterIdentity = require( "./api/TwitterIdentity.js");


// public functions

var kOauth_token = "";
var kOauth_secret = "";

function IsJsonString(str)
{
  try
  {
    JSON.parse(str);
  }
  catch (e)
  {
    return false;
  }
  return true;
}

function LogIn( kConnection)
{
  kOAuth.getOAuthRequestToken(function ( kErrorObject, oauth_token,
    oauth_token_secret, kResultObject)
  {
    if (kErrorObject)
    {
      SendErrorMessage( kConnection, kErrorObject);
      console.log( kErrorObject);
    }
    else
    {
      console.log( kResultObject);

      kOauth_token = oauth_token;
      kOauth_secret = oauth_token_secret;

      var url = "https://api.twitter.com/oauth/authenticate?oauth_token="
        + kOauth_token;

      const kMessage = Buffer.from("{ \"Command\" : \"Login\", \"url\": \""
      + url + "\"}");

      kConnection.sendBytes(kMessage);
    }
  });
}

function VerifyLogIn( kOAuthVerifier, kHashFilter, kConnection)
{
  kOAuth.getOAuthAccessToken( kOauth_token, kOauth_secret, kOAuthVerifier,
    function ( kErrorObject, oauth_access_token, oauth_access_token_secret,
      kResultsObject)
    {
      if ( kErrorObject)
      {
        SendErrorMessage( kConnection, kErrorObject);
        console.log( kErrorObject);
      }
      else
      {
        console.log( kResultsObject);
        console.log( "Authentication Successful");
        console.log( "Incomming HashFilter: "+kHashFilter);

        let kTwitterClient = new TwitterIdentity ( kConnection,
                                                   kHashFilter);

        kTwitterClient.initTwitter( oauth_access_token,
                                    oauth_access_token_secret);

        kLoggedUsers[kConnection.remoteAddress] = kTwitterClient;

        const kMessage = Buffer.from("{ \"Command\" : \"Tokens\", \"OAuthToken\": \""
          + oauth_access_token + "\", \"OAuthTokenSecret\" : \""
          + oauth_access_token_secret + "\"}");
  
        kConnection.sendBytes( kMessage);
  
      }
    }
  );
}

function LogInWithToken( kOAuthToken,
                         kOAuthTokenSecret,
                         kHashFilter,
                         kConnection)
{
  console.log( "Incomming HashFilter: " + kHashFilter);

  let kTwitterClient = new TwitterIdentity ( kConnection,
                                             kHashFilter);

  kTwitterClient.initTwitter( kOAuthToken, kOAuthTokenSecret);

  kLoggedUsers[kConnection.remoteAddress] = kTwitterClient;
}

function LogOff( kConnection)
{
  if ( kConnection.remoteAddress in kLoggedUsers)
  {
    if ( kLoggedUsers[kConnection.remoteAddress].m_bTwitterInitialized)
    {
      kLoggedUsers[kConnection.remoteAddress].unregisterStream();

      kLoggedUsers[kConnection.remoteAddress] = null;
      
      delete kLoggedUsers[kConnection.remoteAddress];
    }
  }
}

function LikeTweet( kConnection, kCommandObject)
{
  if ( CheckValue( kCommandObject, "TweetId"))
  {
    let kId = kCommandObject.TweetId;

    if ( kConnection.remoteAddress in kLoggedUsers)
    {
      kLoggedUsers[kConnection.remoteAddress].favoriteTweet(kId);
    }
    else
    {
      SendErrorMessage( kConnection,
        "You have to be logged in to favorite a tweet.");        
    }
  }
  else
  {
    SendErrorMessage( kConnection, "No TweedId found.");
  }
}

function PostTweet( kConnection, kCommandObject)
{
  if ( CheckValue( kCommandObject, "Text"))
  {
    let kId = kCommandObject.TweetId;

    if ( kConnection.remoteAddress in kLoggedUsers)
    {
      kLoggedUsers[kConnection.remoteAddress].favoriteTweet(kId);
    }
    else
    {
      SendErrorMessage( kConnection,
        "You have to be logged in to post a tweet.");        
    }
  }
  else
  {
    SendErrorMessage( kConnection, "No Text property found.");
  }
}
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
}

function SendErrorMessage(kConnection, kErrorMsg)
{
  kConnection.sendBytes( Buffer.from("{ \"Error\" : \""+ kErrorMsg +"\"}"));
}

// *****************************************************************************
// ************************** HTTP Server **************************************
// *****************************************************************************
let kServer = kHttp.createServer( function( kRequest, kResponse)
{
  // process HTTP request. Since we're writing just WebSockets
  // server we don't have to implement anything.
});

kServer.listen(kWebsocketServerPort, function()
{
  console.log( ( new Date()) + " Server is listening on port "
		        + kWebsocketServerPort);
});

// *****************************************************************************
// ************************** Websocket Server *********************************
// *****************************************************************************
let kWsServer = new kWebSocketServer(
{
  httpServer: kServer
});

kWsServer.on( 'request', function(kRequest)
{
  console.log( ( new Date()) + ' Connection from origin '
		        + kRequest.origin + '.');

  let kConnection = kRequest.accept(null, kRequest.origin);
  
  let iIndex = kClients.push(kConnection) - 1;

  console.log( ( new Date()) + ' Connection accepted.');

  // This is the most important callback for us, we'll handle
  // all messages from users here.
  kConnection.on('message', function( kMessage)
  {
    if (kMessage.type === 'binary')
    {
      let kTempBuffer = Buffer.from( kMessage.binaryData);
      
      let kJsonString = kTempBuffer.toString('UTF8');
  
      if ( !IsJsonString( kJsonString))
      {
        return;
      }

      let kCommandObject = JSON.parse( kJsonString);

      switch ( kCommandObject.Command)
      {
        case "like":
         LikeTweet( kConnection, kCommandObject);
        break; 

        case "post":
         PostTweet( kConnection, kCommandObject);
        break; 

        case "login":
          LogIn( kConnection);
        break; 

        case "verifylogin":
          if ( CheckValue( kCommandObject, "OAuthVerifier") &&
               CheckValue( kCommandObject, "HashFilter"))
          {
            VerifyLogIn( kCommandObject.OAuthVerifier,
                         kCommandObject.HashFilter,
                         kConnection);
          }
          else
          {
            SendErrorMessage( kConnection,
                              "OAuthVerifier or Hashfilter not found.");
          }
        break; 

        case "loginwithtoken":
          if ( CheckValue( kCommandObject, "OAuthToken") &&
               CheckValue( kCommandObject, "OAuthTokenSecret") &&
               CheckValue( kCommandObject, "HashFilter"))
          {
            LogInWithToken( kCommandObject.OAuthToken,
                            kCommandObject.OAuthTokenSecret,
                            kCommandObject.HashFilter,
                            kConnection);
          }
          else
          {
            SendErrorMessage( kConnection,
                              "OAuthToken, OAuthTokenSecret or " +
                              "Hashfilter not found.");
          }
        break; 

        case "logoff":
          LogOff( kConnection);
        break; 

        case "ping":
          SendErrorMessage( kConnection, "pong!");
        break; 

        default:
          SendErrorMessage( kConnection, "Command not valid!");
        break; 
      }
    }
  });

  kConnection.on( 'close', function( kConnection)
  {
    // close user connection
    console.log( ( new Date()) + " Peer "
      + kConnection.remoteAddress + " disconnected.");

    // remove user from the list of connected clients
    kClients.splice(iIndex, 1);
  });

});
