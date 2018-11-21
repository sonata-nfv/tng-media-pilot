'use strict'

module.exports = function(kApp)
{
  let kController = require("../controllers/cmscontroller");

  kApp.route("/registerAggregator")
    .post(kController.RegisterAggregator);
    
  kApp.route("/registerStream")
    .post(kController.RegisterStream);

  kApp.route("/disconnectStream")
    .post(kController.DisconnectStream);

  kApp.route("/getContentList")
    .get(kController.GetContentList);

  kApp.route("/getStreamURL")
    .get(kController.GetStreamURL);

  kApp.route("/registerCamera")
    .post(kController.RegisterCamera);
  };