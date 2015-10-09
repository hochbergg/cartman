import sys
import os
import braintree

from flask import Flask, json
from flask.ext.mongoengine import MongoEngine

from lib.configure import configure_app
from models.all import *

from services.auth.login_service import login_service
from controllers.auth import ctrl as auth_api_ctrl
from controllers.user import ctrl as user_api_ctrl
from controllers.admin import ctrl as admin_ctrl
from controllers.location import ctrl as location_ctrl

# Init braintree

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="7hqsjjpghd965z73",
                                  public_key="t59sfndfpwxjtwsb",
                                  private_key="ed3b633f289b9619826847297192d182")

# Create and initialize the app.
app = Flask(__name__, static_folder="public")
db = MongoEngine()
configure_app(app, db, login_service)

# Register all controllers.
app.register_blueprint(auth_api_ctrl)
app.register_blueprint(user_api_ctrl)
app.register_blueprint(admin_ctrl)
app.register_blueprint(location_ctrl)


if __name__ == "__main__":
  # Run the app.
  app.run()
