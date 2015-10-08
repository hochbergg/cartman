var comm = require("../comm");
var commUtils = require("../lib/comm_utils");
var userComm = require("../../../user_app/app/comm");
var AuthView = require("../models/auth_view");


function AuthController() {
  var self = this;

  /* Initializes the controller, setting up routes and registering the model. */
  this.initialize = function() {
    if (!document.getElementById("auth-page")) {
      return;
    }

    // Construct the underlying model and provide it with a fetcher object for
    // the server data.
    self.model = new AuthView(comm, userComm);
    self.model.initialize();
    self.model.update();

    // Register the model in the view.
    ko.applyBindings(self.model,
                     document.getElementById("auth-page"));

    // Define the controller routes.
    crossroads.addRoute("login:?query:", function(query) {
      fillInQueryParams(query);
      self.model.currentView("login");
    });
    crossroads.addRoute("signup:?query:", function(query) {
      fillInQueryParams(query);
      self.model.currentView("signup");
    });
    crossroads.addRoute("success:?query:", function(query) {
      fillInQueryParams(query);
      self.model.currentView("success");
    });
  };

  /* Returns true if this is a User authentication request. */
  function isUserApp() {
    return document.location.pathname.search("^/auth/user") >= 0;
  }

  /* Returns true if this is an Admin authentication request. */
  function isAdminApp() {
    return document.location.pathname.search("^/auth/admin") >= 0;
  }

  function fillInQueryParams(query) {
    if (!query) {
      return;
    }

    if (query.err && query.err != "null") {
      self.model.error(
        decodeURIComponent(commUtils.decodeURI(query.err)));
    }
    if (query.msg) {
      self.model.infoMessage(
        decodeURIComponent(commUtils.decodeURI(query.msg)));
    }
    if (query.next) {
      self.model.next(
        decodeURIComponent(commUtils.decodeURI(query.next)));
    }
    if (query.user) {
      self.model.setUsername(
        decodeURIComponent(commUtils.decodeURI(query.user)));
    }
  }

  /* Updates the model and view by fetching data from the server. */
  self.update = function() {
  };
}

module.exports = AuthController;
