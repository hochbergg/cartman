from flask import g, redirect, request
from flask.ext.login import current_user
from functools import wraps

from models.login import Login
from services.auth.login_service import login_service


def authorized_for(role, enforce=True, active=Login.ActiveLevel.ACTIVE):
  """
  A decorator that verifies that the wrapped routing function is authorized for
  the given Role.
  Optionally, if the enforce flag is False, doesn't enforce the authorization
  process (this may be used as a way to populate the credentials if they exist,
  but still allow access if they don't).
  Optionally, if the active flag is False, allows non-active Logins to access as
  well (default is True, to enforce only active users in the path).
  """
  def wrapper(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
      if (enforce and
          not login_service.isLoginAuthorizedFor(current_user, role, active)):
        return login_service.login_manager.unauthorized()

      login_service.populateGlobalLoginDetails(current_user)

      return fn(*args, **kwargs)

    return decorated_view

  return wrapper

def update_login_access(fn):
  """
  Decorator that updates the login access (currently only the timestamp).
  """
  @wraps(fn)
  def decorated_view(*args, **kwargs):
    login_service.updateLoginAccess(current_user)
    return fn(*args, **kwargs)

  return decorated_view
