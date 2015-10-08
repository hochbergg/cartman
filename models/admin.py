import datetime
from mongoengine import *

from lib.id_generator import randomIdGenerator
from login import Login


class Admin(Document):
  """
  This model represents an Admin (System administrator) in the database.

  Contains login credentials to log in to the system.
  """
  admin_id = StringField(primary_key=True,
                         default=randomIdGenerator("ADMIN"))

  login = ReferenceField(Login)

  creation_time = DateTimeField(default=datetime.datetime.now)

  def toMinimalJson(self):
    data = self.to_mongo()
    return {
      "adminId": str(self.admin_id),
      "username": str(self.login.username) if self.login else None,
    }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
      "authenticated": str(self.login.authenticated) if self.login else False,
    })
    return json

  def __str__(self):
    return "(%(admin_id)s) [%(creation_time)s]" % self._data

  def __repr__(self):
    return self.__str__()
