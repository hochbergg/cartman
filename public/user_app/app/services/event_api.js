var $ = require("../../../../node_modules/jquery");
window.jQuery = $;
var result = require("../../../bower_components/jpillora/jquery.rest/dist/1/jquery.rest");
var comm_utils = require("../../../auth_app/app/lib/comm_utils");
var serverComm = new $.RestClient(
  "/api/user/", {request: comm_utils.request});

// Add the relevant paths.
serverComm.add("info");

function EventAPI() {
  var self = this;

  self.timers = {};

  self.startTimer = function(id) {
    self.timers[id] = new Date();
  };

  self.stopTimer = function(id) {
    var currentTime = new Date();
    self.timers[id] = currentTime.getTime() - self.timers[id].getTime();
    console.log("Stopping timer for: " + id);
    console.log(self.timers[id].toString() + " ms");
    console.log((self.timers[id] / 1000.0).toString() + " sec");
  };

  self.send = function(name, event) {
    console.log("Got new event from game:");
    console.log(name);
    console.log(event);
  };

}

global.event_api = new EventAPI();
