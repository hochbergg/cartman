var comm = require("../comm");
var MainModel = require("../models/main");

function MainController() {
  var self = this;

  /* Initializes the controller, setting up routes and registering the model. */
  this.initialize = function() {
    if (!document.getElementById("main-page")) {
      return;
    }

    // Construct the underlying model and provide it with a fetcher object for
    // the server data.
    self.model = new MainModel(comm);
    self.model.initialize();
    self.model.update();

    // Register the model in the view.
    ko.applyBindings(self.model,
                     document.getElementById("main-page"));

    // Define the controller routes.
    crossroads.addRoute("/", function() {
      self.model.update();
      self.model.currentView("home");
    });
    crossroads.addRoute("trivia", function() {
      self.model.update();
      self.model.currentView("trivia");
    });
    crossroads.addRoute("profile", function() {
      self.model.update();
      self.model.currentView("profile");
    });
  };

  /* Updates the model and view by fetching data from the server. */
  self.update = function() {
    self.model.update();
  };

}

module.exports = MainController;
