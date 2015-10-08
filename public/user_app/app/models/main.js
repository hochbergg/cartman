var User = require("./user");
var GameView = require("./game_view");


function MainModel(source) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  // Flag for blocking double initializations.
  self.isInitialized = false;

  /* -- Public Methods -- */

  /* Sets up the fields and models. */
  self.initialize = function () {
    // Prevent double initializations.
    if (self.isInitialized) {
      return;
    }

    self.navbar = ko.observable("navbar");

    // The current view to display.
    self.currentView = ko.observable("home");

    // The current User to display and pass on to other views.
    self.user = ko.observable(null);

    self.gameModel = new GameView(self.source);
    self.gameModel.initialize();

    self.topBar = {
      name: ko.pureComputed(function () {
        var user = self.user();
        return user ? user.name : "";
      }),
      loginActivated: ko.pureComputed(function () {
        var user = self.user();
        return user ? user.loginActivated : false;
      }),
    };

    self.fp = {
      email: "play@feuerstein.com"
    };

    // Done initializing.
    self.isInitialized = true;
  };

  /* Fetches new data from the server and updates the model. */
  self.update = function () {
    // Update the debt list model and user parameters from the source.
    self.source.info.read()
      .fail(function (error) {
        console.log("Error occured at /api/user/info/:");
        console.log(error);
      })
      .done(function (data) {
        // Check for errors or missing data.
        if (!data || !data.info) {
          console.log("Invalid data returned from /api/user/info/:");
          console.log(data);
          return;
        }

        // Construct the User model from the data.
        self.user(new User(data.info));
      });

  };
}

module.exports = MainModel;
