import datetime
from mongoengine import *
from flask.ext.login import UserMixin

from lib.id_generator import randomIdGenerator
from login import Login
from user_session import UserSession
from user_session_configuration import UserSessionConfiguration


class User(Document):
  """
  This model represents a User in the database.

  It contains all of the information we have on a specific user, along with
  profile information to be used by communication and collection algorithms.
  """
  user_id = StringField(primary_key=True,
                        default=randomIdGenerator("U"))

  login = ReferenceField(Login)

  creation_time = DateTimeField(default=datetime.datetime.now)

  current_session = ReferenceField(UserSession)
  previous_sessions = ListField(ReferenceField(UserSession))

  user_session_configuration = ReferenceField(UserSessionConfiguration)

  def set_session(self, session):
    if self.current_session:
      self.previous_sessions.append(self.current_session)
    self.current_session = session

  def toMinimalJson(self):
    return {
        "userId": str(self.user_id),
        "username": str(self.login.username) if self.login else None,
        "loginActivated": (bool(self.login.active)
                           if self.login and self.login.active else None),
        "needsActivation": (bool(self.login.needs_activation)
                            if self.login and self.login.needs_activation else None),
        "authenticated": (bool(self.login.authenticated)
                          if self.login and self.login.authenticated else None),
      }

  def toFullJson(self):
    return self.toMinimalJson()

  def __str__(self):
    return "(%(user_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
