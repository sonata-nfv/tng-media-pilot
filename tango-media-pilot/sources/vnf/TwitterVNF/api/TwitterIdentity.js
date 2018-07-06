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

"use strict";

var kTwitter = require('twitter');
const kTwitterConsumerKey = 'PmDsgj3ORwTX7TWjEp1aUcUpr';
const kTwitterConsumerSecret =
  'YkKjnVRzsYwMnqunlco0g8IXbHd5NK0EQm66jj289QJf9wh7mq';

module.exports = class TwitterIdentity
{
  constructor( kConnection, kHashFilter)
  {
    this.m_kConnection = kConnection;
    this.m_kTwitterClient = null;
    this.m_kHashFilter = kHashFilter;
    this.m_bTwitterInitialized = false;
    this.m_kCurrentStream = null;
  }

  initTwitter( kOAuthAccessToken, kOAuthAccessTokenSecret)
  {
	  this.m_kTwitterClient = new kTwitter({
      consumer_key: kTwitterConsumerKey,
      consumer_secret: kTwitterConsumerSecret,
      access_token_key: kOAuthAccessToken,
      access_token_secret: kOAuthAccessTokenSecret
    });

    this.m_bTwitterInitialized = true;

    this.registerStream();
  }

  favoriteTweet( kTweetId)
  {
    if ( !this.m_bTwitterInitialized)
    {
      console.log( "Error: No valid User is logged in.");
      return;
    }

    let CONNECTION = this.m_kConnection;
    this.m_kTwitterClient.post( 'favorites/create', { id: kTweetId + ''},
      function ( kErrorObject, kResponseObject)
      {
        // If the favorite fails, log the error message
        if ( kErrorObject)
        {
          console.log( kErrorObject[0].message);
        }
        // If the favorite is successful, log the url of the tweet
        else
        {
          const kMessage = Buffer.from(JSON.stringify(kResponseObject));

          CONNECTION.sendBytes( kMessage);

          let kUsername = kResponseObject.user.screen_name;

          let kFavoredTweetId = kResponseObject.id_str;
          
          console.log( 'Favorited: ',
            `https://twitter.com/${kUsername}/status/${kFavoredTweetId}`);
        }
      }
    );
  }

  postTweet( kMessage)
  {
    if ( !this.m_bTwitterInitialized)
    {
      console.log( "Error: No valid User is logged in.");
      return;
    }

    let CONNECTION = this.m_kConnection;
    this.m_kTwitterClient.post( 'statuses/update', { status: kMessage+''},
      function(kErrorObject, kTweet, kResponseObject)
      {
        if(kErrorObject)
        {
          console.log(kErrorObject[0].message);
        }
        else
        {
          const kMessage = Buffer.from(JSON.stringify(kResponseObject));

          CONNECTION.sendBytes( kMessage);

          console.log( "tweeted!");
        }
      }
    );
  }

  unregisterStream()
  {
    console.log(this.m_kCurrentStream);

    this.m_kCurrentStream.destroy();

    this.m_kCurrentStream = null;
  }

  registerStream()
  {
    if ( !this.m_bTwitterInitialized)
    {
      console.log( "Error: No valid User is logged in.");
      return;
    }

    console.log( "HashFilter: "+this.m_kHashFilter);

    let CONNECTION = this.m_kConnection;
    let self = this;
    this.m_kTwitterClient.stream('statuses/filter', { track:this.m_kHashFilter},
      function( kStreamObject)
      {
        self.m_kCurrentStream = kStreamObject;

        kStreamObject.on('data', function( kTweetObject)
        {
          kTweetObject["Command"] = "Tweet";
          
          const kMessage = Buffer.from(JSON.stringify( kTweetObject));

          CONNECTION.sendBytes( kMessage);
          
          console.log(kTweetObject.text+"\n");
        });
  
        kStreamObject.on('error', function(kErrorObject)
        {
          console.log(kErrorObject);

          const kMessage = Buffer.from(JSON.stringify(kErrorObject));

          CONNECTION.sendBytes( kMessage);
        });
      }
    );
  }
};