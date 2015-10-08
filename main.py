import sys
import os

from flask import Flask, json
from flask.ext.mongoengine import MongoEngine

from lib.configure import configure_app
from models.all import *

from services.auth.login_service import login_service
from controllers.auth import ctrl as auth_api_ctrl
from controllers.user import ctrl as user_api_ctrl
from controllers.admin import ctrl as admin_ctrl

# Create and initialize the app.
app = Flask(__name__, static_folder="public")
db = MongoEngine()
configure_app(app, db, login_service)

# Register all controllers.
app.register_blueprint(auth_api_ctrl)
app.register_blueprint(user_api_ctrl)
app.register_blueprint(admin_ctrl)

@app.route('/')
def hello():
    return json.jsonify(msg='hello world!')

if __name__ == "__main__":
  # Run the app.
  app.run()
