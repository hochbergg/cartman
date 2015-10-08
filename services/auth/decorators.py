from flask import g, redirect, request
from functools import wraps

from models.login import Login
from services.auth.login_service import login_service


def authorized_for(role, enforce=True):
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
      login = login_service.loadLoginFromRequest(request)

      if (enforce and
          not login_service.isLoginAuthorizedFor(login, role)):
        return login_service.handleUnauthorized(request)

      login_service.populateGlobalLoginDetails(login)

      return fn(*args, **kwargs)

    return decorated_view

  return wrapper
