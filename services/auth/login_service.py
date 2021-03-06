import bcrypt
import datetime
from flask import abort, g, redirect, request
from flask.ext.login import (current_user, LoginManager,
                             login_user, logout_user,
                             user_login_confirmed, user_logged_in,
                             user_accessed)
from flask.signals import Namespace
from itsdangerous import URLSafeTimedSerializer
import re

from models.login import Login
from models.user import User
from services.auth.token_service import token_service

import braintree

class LoginService:
  """
  Handles the Login class during login, logout and persistence of sessions with
  session cookies.

  It allows different roles to have different token timeouts, both for active
  sessions and for global sessions.
  """
  def configure(self, app):
    """
    Configures the various timeouts and flags for each of the roles.
    """
    # Initialize the token service used within.
    token_service.configure(app.config)
    
  def performLoginFromCredentials(self, username, password, push_token=None):
    """
    Handles the login process for the given username and password, rejecting or
    logging in the respective Login model.
    Returns the Login model that was logged in, or None if login failed.
    """
    # Check if the credentials match.
    login = self._fetchLoginByUsername(username)
    if (not login or
        not self._isLoginPasswordMatch(login, password)):
      raise Exception("Incorrect username or password.")

    # Mark the Login as authenticated. 
    login.authenticated = True
    login.push_token = push_token
    login.save()
    
    return token_service.generateToken(login)

  def performLogout(self, login):
    """
    Logs out the given Login model.
    """
    # Mark the Login as not authenticated.
    login.authenticated = False
    login.save()

  def performUserSignup(self, username, password, payment_nonce):
    """
    Signs up the User with the given username and password.
    """
    # First check if the user already in the database.
    user_login = self._fetchLoginByUsername(username)
    if user_login:
      raise Exception("User '%s' already exist.<br>"
                      "Please contact us for more information."
                      % username)

    user_login = Login(username=username)
    # Get the hash of the given password to store in the database.
    pass_hash = self._getHashedPassword(str(password))

    # Create a customer object in BrainTree
    result = braintree.Customer.create({
      "first_name": username,
      "last_name": "User",
      "payment_method_nonce": payment_nonce,
      "id": username,
    })

    if not result.is_success:
      raise Exception("Could not create BrainTree customer")

    # Save the User credentials in the databae.
    user_login.password_hash = pass_hash
    user_login.urole = int(Login.Role.USER)
    user_login.save()

    return user_login

  def loadLoginFromID(self, login_id):
    """
    Returns the Login corresponding to the given login ID.
    """
    # Check if the Login is valid under the various timeout conditions.
    login = self._fetchLogin(login_id)
    if not self._isLoginValid(login):
      return None

    return login

  def loadLoginFromToken(self, token_data):
    """
    Loads the token from the given serialized token data, returning the Login
    that matches or None if no match.
    """
    # First, get the deserialized data from the token using token_service.
    try:
      (username, password_hash) = token_service.loadToken(token_data)
    except Exception, e:
      print "ERROR: LoginService.loadLogin failed to deserialize token: %s" % e
      return None

    # Fetch the corresponding Login object.
    try:
      login = Login.objects(username=username, password_hash=password_hash).get()
    except Exception, e:
      print "ERROR: LoginService.loadToken failed to load Login: %s" % e
      return None

    return login

  def loadLoginFromRequest(self, request):
    """
    Loads the login credentials from the access_token field in the request JSON.
    """
    json = request.get_json(force=True, silent=True)
    if not json:
      json = request.values
    if not json:
      return None

    token_data = json.get("access_token")
    if not token_data:
      return None

    return self.loadLoginFromToken(token_data)

  def isLoginAuthorizedFor(self, login, role):
    """
    Returns True if the given Login is authorized for the given role and the
    optional enforcement of it being active.
    """
    # Check if the Login is actually authenticated.
    if not login or not login.is_authenticated():
      return False

    # Verify that the role has the correct permissions.
    login_role = login.get_role()
    if (login_role != role and
        role != Login.Role.ANY and
        login_role != Login.Role.ADMIN):
      return False

    return True

  def populateGlobalLoginDetails(self, login):
    """
    Populates the Login details in the global Flask object g.
    """
    # The Login object itself.
    g.login = login if not login.is_anonymous() else None

    # Populate the User and Admin.
    g.user = login.user if g.login else None
    g.admin = login.admin if g.login else None

  def handleUnauthorized(self, request):
    # API requests are rejected with an error if not authorized.
    if request.path.startswith("/api"):
      abort(401)

    # Redirect to the correct login according to the role.
    if request.path.startswith("/admin"):
      role = "admin"
    elif request.path.startswith("/user"):
      role = "user"
    else:
      # If we have no match, this is an invalid request.
      abort(404)
    return redirect("/auth/%s/#login?next=%s" % (role, request.path))

  def _isLoginPasswordMatch(self, login, password):
    """
    Validates the given password for the given login.
    """
    return (login and
            self._isPasswordMatch(password, login.password_hash))

  def _isLoginValid(self, login):
    """
    Checks if the Login is valid.
    """
    if not login:
      return False

    return True

  def _isPasswordMatch(self, plain_text_password, hashed_password):
    """
    Checks the hased password against the given plain text password.
    Using bcrypt, the salt is saved into the hash itself.
    Returns True if plain_text_password == hashed_password.
    """
    try:
      return bcrypt.checkpw(plain_text_password, hashed_password)
    except Exception, e:
      raise e

  def _getHashedPassword(self, plain_text_password):
    """
    Returns a hashed password (using bcrypt) of the given plain text password.
    """
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

  def _fetchLogin(self, login_id):
    """
    Fetches the Login model by ID.
    """
    try:
      return Login.objects(login_id=login_id).get()
    except:
      return None

  def _fetchLoginByUsername(self, username, password_hash=None):
    """
    Fetches the Login model corresponding to the given username.
    If an optional password_hash is given, verifies that the password hash
    matches as well.
    """
    try:
      if password_hash is None:
        return Login.objects(username=username).get()
      else:
        return Login.objects(username=username,
                             password_hash=password_hash).get()
    except:
      return None

# Initialize the singleton service itself.
login_service = LoginService()
