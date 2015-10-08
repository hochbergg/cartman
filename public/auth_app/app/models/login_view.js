/**
 * Created by shaked on 3/26/15.
 */


function LoginView(source, authModel) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  // Main auth model.
  self.authModel = authModel;

  // The URL to send to the server for redirection after successful login.
  self.next = authModel.next;
  // Editable text input for username.
  self.username = authModel.username;
  // Editable text input for password.
  self.password = ko.observable();
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
  self.login = function() {
    self.source.login.create(getEditableComponents())
        .done(function(result) {
          if (result.err) {
            console.log("LoginView.login failed:");
            console.log(result.err);
            self.error("<strong>Login Failed!</strong> " + result.err);
            self.message(null);
            return;
          }

          self.message("Successfully logged in!");
          self.error(null);

          var next = result.next.replace("!", "#");
          window.location.assign(next);
        })
        .fail(function(error) {
          console.log("LoginView.login failed:");
          console.log(error);
          self.error("<strong>Login Failed!</strong><br> " +
                     "Username or Password incorrect.<br>" +
                     "Or User is not activated in the system yet.");
          self.message(null);
        });
  };

  /* Returns an object with the data from all the editable fields for sending to
   * the server when login. */
  function getEditableComponents() {
    return {
        username: self.username(),
        password: self.password(),
        next: self.next(),
      };
  }
}

module.exports = LoginView;
