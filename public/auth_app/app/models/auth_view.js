var LoginView = require("./login_view");
var SignupView = require("./signup_view");
var SuccessView = require("./success_view");
var commUtils = require("../lib/comm_utils");


function AuthView(source, sourceToUser) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  self.sourceToUser = sourceToUser;

  // Flag for blocking double initializations.
  self.isInitialized = false;

  /* -- Public Methods -- */

  /* Sets up the fields and models. */
  self.initialize = function() {
    // Prevent double initializations.
    if (self.isInitialized) {
      return;
    }

    // The current view to display.
    self.currentView = ko.observable("login");
    // The current view to display in the navbar template.
    self.navbar = ko.observable("navbar");

    // The current User to display and pass on to other views.
    self.user = ko.observable(null);
    // The current Client to display and pass on to other views.
    self.client = ko.observable(null);

    // The login information for the currently logged in user (if any).
    self.loginInfo = ko.observable(null);
    // The business info for the client.
    self.businessInfo = ko.observable(null);

    // Top bar data to display, based on self.user.
    self.topBar = {
      name: ko.pureComputed(function() {
        var user = self.user();
        return user ? user.name : "";
      }),
      loginActivated: ko.pureComputed(function () {
        var user = self.user();
        return user ? user.loginActivated : false;
      }),
    };

    // The username to login or signup with.
    self.username = ko.observable();
    // The next URL to redirect to after the process.
    self.next = ko.observable();
    // The message to display to the user from web query.
    self.infoMessage = ko.observable();
    // The error to display to the user from web query.
    self.error = ko.observable();
    // Sets and gets the focus status of the username field.
    self.isUsernameFocus = ko.observable(true);
    // Sets and gets the focus status of the password field.
    self.isPasswordFocus = ko.observable(false);

    // The brand name to display.
    self.brandName = ko.pureComputed(function() {
      // TODO: Make this return a 404 is case there is no brandName
      return self.businessInfo() ? self.businessInfo().brandName() : "";
    });

    // The HTML of the brand name to display on the page.
    self.brandNameHtml = ko.pureComputed(function() {
      // TODO: Make this return a 404 is case there is no brandName
      return self.businessInfo() ? self.businessInfo().brandNameHtml() : "";
    });

    // True if there is a brand to display.
    self.hasBrand = ko.pureComputed(function() {
        return self.businessInfo() != null;
    });

    // Always false to display the correct navbar options (on User).
    self.loggedIn = ko.pureComputed(function() {
      return false;
    });

    /* Always false to disable all possible views (on Client). */
    self.isViewAccessible = function(view) {
      return false;
    };

    // Sets username and focus in form fields.
    self.setUsername = function(username) {
      self.username(username);
      self.isPasswordFocus(true);
    };

    // View model for success page after sign-up.
    self.successModel = new SuccessView(self.source, self);
    // View model for login page.
    self.loginModel = new LoginView(self.source, self);
    // View model for sign-up page.
    self.signupModel = new SignupView(self.source, self, self.successModel);

    // Done initializing.
    self.isInitialized = true;
  };

  self.update = function() {
    // Update the business info with the brand and logo.
    if (self.isUserApp) {
      // Read the User info.
      self.source.login.info.read()
        .fail(function (error) {
          console.log("Error occured at /auth/login/info/:");
          console.log(error);
          notification_view.notifyError(
            "<strong>Update from server failed!</strong> " +
            "Try refreshing the page.");
        })
        .done(function (data) {
          // Check for errors or missing data.
          if (!data) {
            console.log("Invalid data returned from /auth/login/info/:");
            console.log(data);
            return;
          }

          // Save the login info.
          var info = data.info;
          self.loginInfo(info || null);

          // Save the username if we have one.
          if (info && info.username) {
            self.setUsername(info.username);
          }

          // Redirect to signup page if the user is not yet active.
          if (info && !info.active) {
            redirectToPage("/auth/user/#signup",
                           self.next(),
                           self.username(),
                           self.error(),
                           self.infoMessage());
          }
        });
    }
  };

  // Sets the static method to be a instance method.
  self.redirectToPage = redirectToPage;

}

/* Redirects to the given auth page with the given query parameters. */
function redirectToPage(page, next, username, error, message) {
  var urlElements = [];
  if (next) {
    urlElements.push("next=" + commUtils.encodeURIComp(next));
  }
  if (username) {
    urlElements.push("user=" + commUtils.encodeURIComp(username));
  }
  if (error) {
    urlElements.push("err=" + commUtils.encodeURIComp(error));
  }
  if (message) {
    urlElements.push("msg=" + commUtils.encodeURIComp(message));
  }
  var query = urlElements.join("&");

  var url = page;
  if (query) {
    url += "?" + query;
  }

  window.location.assign(url);
}
AuthView.redirectToPage = redirectToPage;

module.exports = AuthView;
