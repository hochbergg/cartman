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


class LoginService:
  """
  Handles the Login class during login, logout and persistence of sessions with
  session cookies.

  It allows different roles to have different token timeouts, both for active
  sessions and for global sessions.
  """
  def __init__(self):
    """
    Initializes the LoginService with its internal LoginManager.
    """
    # Create the login manager we will use through the service.
    self.login_manager = LoginManager()

    # Initialize signals that wrap and adapt Flask-Login signals.
    self.signal_namespace = Namespace()
    self.new_session = self.signal_namespace.signal("new-session")

  def configure(self, app):
    """
    Configures the various timeouts and flags for each of the roles.
    """
    # Import configuration parameters for tokens.
    role_settings = app.config.get("TOKEN_ROLE_SETTINGS", {})
    self.role_settings = { Login.Role(role): settings
                           for (role, settings) in role_settings.items() }
    self.use_subdomains = app.config.get("WEB_USE_SUBDOMAINS")

    # Initialize the token service used within.
    token_service.configure(app.config)
    
    # Initialize the LoginManager.
    self.login_manager.init_app(app)
    self.login_manager.session_protection = "strong"

    # Register for Flask-Login related signals.
    @user_logged_in.connect_via(app)
    @user_login_confirmed.connect_via(app)
    def handle_user_logged_in(app, user=None, **extras):
      login = user or g.login
      role = login.get_role() if login else None
      self.new_session.send(self, login=login, role=role, **extras)

  def performLoginFromCredentials(self, username, password):
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
    login.save()

    # Log in the user in Flask-Login.
    login_user(user=login, remember=True)

    # Update the last access time.
    self.updateLoginAccess(login)
    
    return login

  def performLogout(self, login):
    """
    Logs out the given Login model.
    """
    # Mark the Login as not authenticated.
    login.authenticated = False
    login.save()

    # Log out the user in Flask-Login.
    logout_user()

  def performUserSignup(self, username, password):
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
    pass_hash = login_service._getHashedPassword(str(password))

    # Save the User credentials in the databae.
    user_login.password_hash = pass_hash
    user_login.active = True
    user_login.activation_time = datetime.datetime.now()
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

  def isLoginAuthorizedFor(self, login, role, active=Login.ActiveLevel.ACTIVE):
    """
    Returns True if the given Login is authorized for the given role and the
    optional enforcement of it being active.
    """
    # Check if the Login is actually authenticated.
    if not login.is_authenticated():
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

  def updateLoginAccess(self, login):
    """
    Updates the last access time for the given Login instance.
    This is important if session timeouts are needed, as this needs to be called
    to indicate activity in the Login whenever an event that is considered to be
    activity occurs.
    """
    if login.is_authenticated():
      login.last_access_time = datetime.datetime.now()
      login.save()

  def _isLoginPasswordMatch(self, login, password):
    """
    Validates the given password for the given login.
    """
    return (login and login.active and
            self._isPasswordMatch(password, login.password_hash))

  def _isLoginValid(self, login):
    """
    Checks if the Login is valid.
    Currently only session timeout is checked.
    """
    if not login:
      return False

    # Get the specific role of the Login.
    role = login.get_role()
    role_settings = self.role_settings.get(role, {})

    # Check the session timeout since last activity was registered.
    session_timeout = role_settings.get("SESSION_TIMEOUT")
    if session_timeout is not None and login.last_access_time is not None:
      seconds_since_last_access = (datetime.datetime.now() -
                                   login.last_access_time).total_seconds()
      if seconds_since_last_access > session_timeout:
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
    except:
      return None

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

@login_service.login_manager.token_loader
def load_token(token):
  return login_service.loadLoginFromToken(token)

@login_service.login_manager.user_loader
def load_login(login_id):
  return login_service.loadLoginFromID(login_id)

@login_service.login_manager.unauthorized_handler
def unauthorized():
  # API requests are rejected with an error if not authorized.
  if request.path.startswith("/api"):
    abort(401)

  # If this is a User specific login, and the associated Login is not active,
  # redirect to the signup page.
  if (request.path.startswith("/auth/user") and
      current_user and
      not current_user.is_anonymous() and
      not current_user.active):
    return redirect("/auth/user/#signup?user=%s&next=%s" %
                    (current_user.username, request.path))

  # Redirect to the correct login according to the role.
  if request.path.startswith("/admin"):
    role = "admin"
  elif request.path.startswith("/user"):
    role = "user"
  else:
    # If we have no match, this is an invalid request.
    abort(404)
  return redirect("/auth/%s/#login?next=%s" % (role, request.path))
