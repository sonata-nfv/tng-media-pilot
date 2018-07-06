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

const PORT = 50001;

var kDgram = require('dgram');
var kUDPServer = kDgram.createSocket('udp4');

var fs = require('fs');
var readline = require('readline');
const {GoogleApis} = require('googleapis');
const {OAuth2Client} = require('google-auth-library');

// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/google-apis-nodejs-quickstart.json
var SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
var TOKEN_DIR = (process.env.HOME || process.env.HOMEPATH ||
    process.env.USERPROFILE) + '/.credentials/';
var TOKEN_PATH = TOKEN_DIR + 'google-apis-nodejs-quickstart.json';

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 *
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, requestData, callback) {
  var clientSecret = credentials.installed.client_secret;
  var clientId = credentials.installed.client_id;
  var redirectUrl = credentials.installed.redirect_uris[0];
  //var auth = new googleAuth();
  var oauth2Client = new OAuth2Client(clientId, clientSecret, redirectUrl);

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, function(err, token) {
    if (err) {
      getNewToken(oauth2Client, requestData, callback);
    } else {
      oauth2Client.credentials = JSON.parse(token);
      callback(oauth2Client, requestData);
    }
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 *
 * @param {google.auth.OAuth2} oauth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback to call with the authorized
 *     client.
 */
function getNewToken(oauth2Client, requestData, callback) {
  var authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES
  });
  console.log('Authorize this app by visiting this url: ', authUrl);
  var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  rl.question('Enter the code from that page here: ', function(code) {
    rl.close();
    oauth2Client.getToken(code, function(err, token) {
      if (err) {
        console.log('Error while trying to retrieve access token', err);
        return;
      }
      oauth2Client.credentials = token;
      storeToken(token);
      callback(oauth2Client, requestData);
    });
  });
}

/**
 * Store token to disk be used in later program executions.
 *
 * @param {Object} token The token to store to disk.
 */
function storeToken(token) {
  try {
    fs.mkdirSync(TOKEN_DIR);
  } catch (err) {
    if (err.code != 'EEXIST') {
      throw err;
    }
  }
  fs.writeFile(TOKEN_PATH, JSON.stringify(token));
  console.log('Token stored to ' + TOKEN_PATH);
}

/**
 * Remove parameters that do not have values.
 *
 * @param {Object} params A list of key-value pairs representing request
 *                        parameters and their values.
 * @return {Object} The params object minus parameters with no values set.
 */
function removeEmptyParameters(params) {
  for (var p in params) {
    if (!params[p] || params[p] == 'undefined') {
      delete params[p];
    }
  }
  return params;
}

/**
 * Create a JSON object, representing an API resource, from a list of
 * properties and their values.
 *
 * @param {Object} properties A list of key-value pairs representing resource
 *                            properties and their values.
 * @return {Object} A JSON object. The function nests properties based on
 *                  periods (.) in property names.
 */
function createResource(properties) {
  var resource = {};
  var normalizedProps = properties;
  for (var p in properties) {
    var value = properties[p];
    if (p && p.substr(-2, 2) == '[]') {
      var adjustedName = p.replace('[]', '');
      if (value) {
        normalizedProps[adjustedName] = value.split(',');
      }
      delete normalizedProps[p];
    }
  }
  for (var p in normalizedProps) {
    // Leave properties that don't have values out of inserted resource.
    if (normalizedProps.hasOwnProperty(p) && normalizedProps[p]) {
      var propArray = p.split('.');
      var ref = resource;
      for (var pa = 0; pa < propArray.length; pa++) {
        var key = propArray[pa];
        if (pa == propArray.length - 1) {
          ref[key] = normalizedProps[p];
        } else {
          ref = ref[key] = ref[key] || {};
        }
      }
    };
  }
  return resource;
}


function searchListByKeyword(auth, requestData) {
  const google = new GoogleApis();
  /*console.log(JSON.stringify(google));
  var service = google.youtube;
  console.log(JSON.stringify(service));*/
  var parameters = removeEmptyParameters(requestData['params']);
  parameters['auth'] = auth;
  google.youtube('v3').search.list(parameters, function(err, response) {
    if (err) {
      console.log('The API returned an error: ' + err);
      return;
    }
    console.log(response);
    const kClient = kDgram.createSocket( 'udp4');
    const kMessage = Buffer.from( JSON.stringify(response.data));
    kClient.send( kMessage, 32100, "192.168.56.1",
      (err) => { kClient.close();});
  });
}

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

function SendErrorMessage(kIpAddress, kErrorMsg)
{
  const kClient = kDgram.createSocket('udp4');

  let kMessage = "";

  if (IsJsonString(kErrorMsg))
  {
    kMessage = Buffer.from( "{ \"Error\" : "+ kErrorMsg +" }");
  }
  else
  {
    kMessage = Buffer.from( "{ \"Error\" : \""+ kErrorMsg +"\"}");
  }

  kClient.send(kMessage, 32100, kIpAddress, (err) => { kClient.close();});
}

// Server Stuff

kUDPServer.on('listening', function ()
{
  let address = kUDPServer.address();
  console.log('UDP Server listening on ' + address.address + ":"
  + address.port);
});

kUDPServer.on('message', function (kMessageObject, kRemoteObject)
{
  let JsonString = kMessageObject.toString();
  
  if (!IsJsonString(JsonString))
    return;

  let kCommandObject = JSON.parse(JsonString);

  switch (kCommandObject.Command)
  {
    case "login":
    {
      //
    }
    break;
    case "search":
    {
      if ( "QueryString" in kCommandObject && kCommandObject.QueryString != null &&
        kCommandObject.QueryString != "")
      {
        let kQueryString = kCommandObject.QueryString;
   
        //if (kRemoteObject.address in kLoggedUsers)
        //{
        //  kLoggedUsers[kRemoteObject.address].favoriteTweet(kId);
        //}
        //else
        //{
        //  SendErrorMessage( kRemoteObject.address, "You have to be logged in to favorite a "
        //               +"tweet.");        
        //}

        // Load client secrets from a local file.
        fs.readFile('client_secret.json', function processClientSecrets(err, content) {
        if (err) {
          console.log('Error loading client secret file: ' + err);
          return;
        }
        // Authorize a client with the loaded credentials, then call the YouTube API.
        //See full code sample for authorize() function code.
        authorize(JSON.parse(content), {'params': {'maxResults': '25',
                 'part': 'snippet',
                 'q': kQueryString,
                 'type': ''}}, searchListByKeyword);
        });
      }
      else
      {
        SendErrorMessage( kRemoteObject.address, "No Querystring found.");
      }
    }
    break;
  }
  
  console.log(kRemoteObject.address + ':' + kRemoteObject.port +' - ' + JsonString);
});

kUDPServer.bind(PORT);