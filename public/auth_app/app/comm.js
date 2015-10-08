var comm_utils = require("./lib/comm_utils");

// Initialize the server communications REST client.
var serverComm = new $.RestClient(
    "/auth/", { request: comm_utils.request });

// Add the relevant paths.
serverComm.add("login", { isSingle: true });
serverComm.login.add("info");
serverComm.add("signup");
serverComm.add("new_account_info");

module.exports = serverComm;
