var commUtils = require("../lib/comm_utils");

function SuccessView(source, authModel) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  // Main auth model.
  self.authModel = authModel;

  // The message to show to the user after an operation.
  self.infoMessage = authModel.infoMessage;
  // The error to show to the user after an operation.
  self.error = authModel.error;
  // The username  of the signed user.
  self.username = authModel.username;
  // The next url for after the login process.
  self.next = authModel.next;

  // The next URL to redirect to on continue.
  self.continueURL = ko.pureComputed(function () {
    if (self.next()) {
      return self.next();
    }

    var url = "#login";
    if (self.username()) {
      url += "?user=" + commUtils.encodeURIComp(self.username());
    }
    return url;
  });
}

module.exports = SuccessView;
