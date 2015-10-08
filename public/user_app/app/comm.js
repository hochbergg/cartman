var comm_utils = require("../../auth_app/app/lib/comm_utils");

// Initialize the server communications REST client.
var serverComm = new $.RestClient(
  "/api/user/", {request: comm_utils.request});

// Add the relevant paths.
serverComm.add("info");

module.exports = serverComm;
