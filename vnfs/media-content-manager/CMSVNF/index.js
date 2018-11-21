'use strict'

let kExpress = require('express'),
  app = kExpress(),
  port = 50000,
  bodyParser = require('body-parser'),
  cors = require('cors');


var whitelist = ['https://resttesttest.com', 'localhost']
var corsOptions = {
  origin: function (origin, callback) {
    if (whitelist.indexOf(origin) !== -1 || !origin) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  }
}
app.options('*', cors()) // include before other routes
app.use(cors(corsOptions));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
  
let routes = require('./api/routes/cmsroutes'); //importing route
routes(app); //register the route

app.listen(port);

console.log('5GTango CMS VNF started on: ' + port);
