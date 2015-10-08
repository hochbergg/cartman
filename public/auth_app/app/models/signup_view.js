var commUtils = require("../lib/comm_utils");

function SignupView(source, authModel, successModel) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  // Main auth model.
  self.authModel = authModel;
  // Success page model.
  self.successModel = successModel;

  // The next uri to redirect after sign up is completed.
  self.next = authModel.next;
  // Editable text input for username.
  self.username = authModel.username;
  // Editable text input for password.
  self.password = ko.observable();
  // Editable text input for password confirm.
  self.passwordRepeat = ko.observable();
  // The message to show to the user after an operation.
  self.infoMessage = authModel.infoMessage;
  // The error to show to the user after an operation.
  self.error = authModel.error;

  // Message to display to the user from web query.
  self.message = ko.observable();
  // The brand name to display.
  self.brandName = authModel.brandName;
  // The brand name as html to display.
  self.brandNameHtml = authModel.brandNameHtml;
  // Define if username field has focus.
  self.isUsernameFocus = authModel.isUsernameFocus;
  // Define if password field has focus.
  self.isPasswordFocus = authModel.isPasswordFocus;

  /* Submits the communication parameter changes to the source. */
  self.signup = function () {
    if (self.username() == null || self.username() == "") {
      self.error("Please insert your username.");
      return;
    }
    else if (self.password() == null || self.password() == "") {
      self.error("Password field cannot be empty.");
      return;
    } else if (self.password().length < 6 || self.password().length > 14) {
      self.error("Password must between 6-14 characters.");
      return;
    } else if (self.passwordRepeat() == null || self.passwordRepeat() == "") {
      self.error("Please insert your password again for confirmation.");
      return;
    } else if (self.password() != self.passwordRepeat()) {
      self.error("Password and retyped password do not match.");
      return;
    }

    self.source.signup.create(getEditableComponents())
      .done(function (result) {
        if (result.err) {
          console.log("SignupView.signup failed on done:");
          console.log(result.err);
          self.error("<strong>Login Failed!</strong> " + result.err);
          self.message(null);
          return;
        }

        self.message(result.msg);
        self.error(null);
        self.successModel.infoMessage(result.successMsg);

        var url = "/auth/user/#success";
        self.authModel.redirectToPage(url, self.next());
      })
      .fail(function (error) {
        console.log("SignupView.signup failed on fail:");
        console.log(error);
        self.error("<strong>Login Failed!</strong><br> " +
          error);
        self.message(null);
      });
  };

  /* Returns an object with the data from all the editable fields for sending to
   * the server when login. */
  function getEditableComponents() {
    return {
      username: self.username(),
      password: self.password(),
    };
  }

}

module.exports = SignupView;
