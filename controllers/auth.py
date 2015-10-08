import bcrypt
from flask import Blueprint, redirect, request, jsonify, g, abort
from flask.ext.login import current_user, login_user, logout_user, LoginManager
import os

from models.login import Login
from services.auth.login_service import login_service


class AuthController(Blueprint):
  """
  This controller responds to Client API calls.

  The get* methods are for returning data for the corresponding API calls.
  The _fetch* methods are for fetching data from the database.
  """
  def getLoginByUsername(self, username):
    """
    Returns the Login model corresponding to the given username.
    """
    return self._fetchLoginByUsername(username)

  def getLoginInfo(self):
    """
    Returns the Login object parameters if currently logged in.
    """
    login = None
    if g.login and not g.login.is_anonymous():
      login = g.login.toFullJson()
    return jsonify(info=login)

  def handleLogin(self, username, password, next_url=""):
    """
    Handles the login process for the given username and password, rejecting or
    logging in the respective login model.
    """
    # Verify we have at least one set of credentials.
    if not username:
      return jsonify(err="Invalid username")
    if not password:
      return jsonify(err="Invalid password")

    # Perform the login process itself.
    try:
      login_obj = login_service.performLoginFromCredentials(username, password)
    except Exception, e:
      return jsonify(err="Incorrect username or password.")

    # If this is an Admin login, redirect to the admin app.
    if login_obj.get_role() == Login.Role.ADMIN:
      return jsonify(next=(next_url or "/admin"))

    # If this is a User login, redirect to the user app.
    if login_obj.get_role() == Login.Role.USER:
      return jsonify(next=(next_url or "/user"))

    # If the role doesn't match anything, it can only be corruption.
    abort(403)

  def handleLogout(self, login_obj):
    """
    Logs out the given Login model.
    """
    login_service.performLogout(login_obj)

  def handleUserSignup(self, username, password):
    """
    Signs up the User with the given username and password.
    """
    # Perform the signup.
    try:
      user_login = login_service.performUserSignup(username, password)
    except Exception, e:
      return jsonify(err=str(e))

    # Login the User automatically.
    try:
      login_obj = login_service.performLoginFromCredentials(username, password)
    except Exception, e:
      return jsonify(err=str(e))

    # Create the message details to return to the User.
    success_message = "Your are now signed up."


    # TODO: Send confirmation mail communication to the User.

    return jsonify(msg=("User '%s' Successfully signed up to the system!"
                        % username)
                        + (" You can now <a href='/auth/user/'>login</a>"),
                   successMsg=success_message)


# Create and initialize the controller for the Auth API.
ctrl = AuthController("authentication", __name__, static_folder="../public")

@ctrl.route("/auth/login/", methods=["POST"])
def auth_login():
  return ctrl.handleLogin(request.form.get("username"),
                          request.form.get("password"),
                          next_url=request.values.get("next"))

@ctrl.route("/auth/user/logout/",
            methods=["POST", "GET"])
@ctrl.route("/auth/admin/logout/",
            methods=["POST", "GET"])
def logout():
  # Determine the role by the login or by the logout path.
  try:
    role = g.login.get_role().name.lower()
  except:
    role = request.path.split("/")[2]

  # Perform the logout, disregarding errors.
  try:
    ctrl.handleLogout(g.login)
  except:
    pass

  return redirect("/%s" % role)

@ctrl.route("/auth/signup/", methods=["POST"])
def user_signup():
  return ctrl.handleUserSignup(request.form.get("username"),
                               request.form.get("password"))

@ctrl.route("/auth/login/info/")
def auth_login_info():
  return ctrl.getLoginInfo()
