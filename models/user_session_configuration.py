import datetime
from mongoengine import *

from game_session_configuration import GameSessionConfiguration
from lib.id_generator import randomIdGenerator


class UserSessionConfiguration(Document):
  """
  This model represents a configuration of a session of a User in the database.

  It is a template for creating a session conmprised of several game session
  configurations.
  """
  user_session_configuration_id = StringField(primary_key=True,
                                              default=randomIdGenerator("USC"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  game_session_configurations = ListField(ReferenceField(GameSessionConfiguration))

  def toMinimalJson(self):
    return {
        "userSessionConfigurationId": str(self.user_session_configuration_id),
        "name": str(self.name),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "game_session_configurations": [gs.toMinimalJson()
                                        for gs in self.game_session_configurations],
    })
    return json

  def __str__(self):
    return "(%(user_session_configuration_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
