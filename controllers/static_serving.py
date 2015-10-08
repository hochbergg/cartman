import os
from flask import Blueprint, g, redirect

from lib.no_cache_decorator import nocache
from models.login import Login
from services.auth.decorators import authorized_for


# Create and initialize the controller for serving the app files.
ctrl = Blueprint("static_serving", __name__, static_folder="../public")

# Authentication app paths.
@ctrl.route("/auth_app/<path:path>")
def auth_app_proxy(path):
    return ctrl.send_static_file(os.path.join("auth_app", path))

# User app paths.
@ctrl.route("/user_app/<path:path>")
def public_user_app_proxy(path):
    return ctrl.send_static_file(os.path.join("user_app", path))

# Admin app paths.
@ctrl.route("/admin_app/<path:path>")
def public_admin_app_proxy(path):
    return ctrl.send_static_file(os.path.join("admin_app", path))

# Common app paths.
@ctrl.route("/common/<path:path>")
def public_common_app_proxy(path):
    return ctrl.send_static_file(os.path.join("common", path))

# Common file paths.
@ctrl.route("/common-files/<path:path>")
def public_common_files_proxy(path):
    return ctrl.send_static_file(os.path.join("common-files", path))
@ctrl.route("/flat-ui/<path:path>")
def public_flat_ui_proxy(path):
    return ctrl.send_static_file(os.path.join("flat-ui", path))
@ctrl.route("/ui-kit/<path:path>")
def public_ui_kit_proxy(path):
    return ctrl.send_static_file(os.path.join("ui-kit", path))
@ctrl.route("/bower_components/<path:path>")
def public_bower_components_proxy(path):
    return ctrl.send_static_file(os.path.join("bower_components", path))
