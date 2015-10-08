import os
from flask import Blueprint, current_app, g, redirect, abort, jsonify

from lib.no_cache_decorator import nocache
from models.login import Login
from services.auth.decorators import authorized_for


# Create and initialize the controller for serving the app files.
ctrl = Blueprint("app_serving", __name__, static_folder="../public")

# Setup client app and static routes.
@ctrl.route("/")
@authorized_for(role=Login.Role.ANY, enforce=False)
def root():
  # If a Client or User were logged in, redirect to relevant app.
  if g.admin:
      return redirect("/admin")

  return redirect("/user")

@ctrl.route("/auth/user/")
@nocache
def auth_user_path():
  return ctrl.send_static_file(os.path.join("user_app", "auth.html"))
  # return ctrl.send_static_file(os.path.join("user_app", "auth.html"))

@ctrl.route("/auth/admin/")
@nocache
def auth_admin_path():
  return ctrl.send_static_file(os.path.join("admin_app", "auth.html"))

@ctrl.route("/user")
@authorized_for(role=Login.Role.USER)
@nocache
def user_path():
  return ctrl.send_static_file(os.path.join("user_app", "index.html"))

@ctrl.route("/admin")
@authorized_for(role=Login.Role.ADMIN)
@nocache
def admin_path():
  return ctrl.send_static_file(os.path.join("admin_app", "index.html"))
