var User = require("./user");


function GameView(source) {
  var self = this;

  // Set the model source from the given one.
  self.source = source;
  // Flag for blocking double initializations.
  self.isInitialized = false;

  /* Sets up the fields and models. */
  self.initialize = function () {
    // Prevent double initializations.
    if (self.isInitialized) {
      return;
    }

    window.onload = function () {
      console.log("Resizing onload.");
      var iframeWin = document.getElementById("game-iframe").contentWindow;
      $(iframeWin).resize();
    };

    self.isInitialized = true;
  };

}

module.exports = GameView;
