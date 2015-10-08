import datetime
from mongoengine import *

from game_session import GameSession
from user_session_configuration import UserSessionConfiguration
from lib.id_generator import randomIdGenerator


class UserSession(Document):
  """
  This model represents a session of a User in the database (comprised of
  potentially several games).

  It contains all of the data, events, markers and interruptions for an entire
  session of games.
  """
  user_session_id = StringField(primary_key=True,
                                default=randomIdGenerator("US"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  user = GenericReferenceField(required=True)
  user_session_configuration = ReferenceField(UserSessionConfiguration)

  game_sessions = ListField(ReferenceField(GameSession))

  def current_game_session(self):
    if not self.game_sessions:
      return None
    return self.game_sessions[-1]

  def next_game_session_configuration(self):
    game_configs = self.user_session_configuration.game_session_configurations
    if not game_configs:
      return None
    return game_configs[len(self.game_sessions)]

  def toMinimalJson(self):
    return {
        "userSessionId": str(self.user_session_id),
        "userId": str(self.user.user_id),
        "userSessionConfigurationId": (
            str(self.user_session_configuration.user_session_configuration_id)
            if self.user_session_configuration else None),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "game_sessions": [gs.toMinimalJson() for gs in self.game_sessions],
    })
    return json

  def __str__(self):
    return "(%(user_session_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
