from flufl.enum import Enum
from mongoengine import *
from flask.ext.login import UserMixin

from lib.id_generator import randomIdGenerator
from services.auth.token_service import token_service

class Login(Document, UserMixin):
  """
  This model represents a persistent login of any user (in the general sense)
  that is registered in the system, and provides flask.ext.login with the
  necessary data and tools to manage the session.
  """
  login_id = StringField(primary_key=True,
                         default=randomIdGenerator("L"))

  username = StringField(unique=True, max_length=50)
  password_hash = BinaryField(required=True)

  needs_activation = BooleanField(default=True)
  active = BooleanField(default=False)
  activation_time = DateTimeField()

  user = GenericReferenceField()
  admin = GenericReferenceField()

  authenticated = BooleanField(default=False)

  last_access_time = DateTimeField()

  class Role(Enum):
    ANY = 0
    USER = 1
    ADMIN = 2
  urole = IntField(default=Role.ANY, choices=Role._enums.keys())

  class ActiveLevel(Enum):
    INACTIVE = 0
    GUEST = 1
    ACTIVE = 2

  def get_active_level(self):
    """Returns the activation level of this login."""
    if self.active:
      return self.ActiveLevel.ACTIVE
    if not self.needs_activation:
      return self.ActiveLevel.GUEST
    return self.ActiveLevel.INACTIVE

  def is_active(self):
    """Returns if the user is active or not."""
    return self.active

  def is_authenticated(self):
    """Return True if the user is authenticated."""
    return self.authenticated

  def is_anonymous(self):
    """False, as anonymous users aren't supported."""
    return False

  def get_auth_token(self):
    """Returns a custom encrypted token of the serialized Login credentials."""
    return token_service.generateToken(self)

  def get_urole(self):
    """Returns the role as an integer."""
    return self.urole

  def get_role(self):
    """Returns the Role as an enum."""
    return self.Role(self.urole) if self.urole is not None else None

  def toMinimalJson(self):
    return {
      "loginId": str(self.login_id),
      "username": str(self.username),
    }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
      "authenticated": str(self.authenticated),
      "needsActivation": self.needs_activation,
      "active": self.active,
    })
    return json

  def __str__(self):
    return "(%(login_id)s) %(username)s" % self._data

  def __repr__(self):
    return self.__str__()
