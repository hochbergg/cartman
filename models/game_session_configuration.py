import datetime
from mongoengine import *

from game import Game
from lib.id_generator import randomIdGenerator


class GameSessionConfiguration(Document):
  """
  This model represents a session of a Game in the database.

  It contains all of the data, events, markers and interruptions of the game.
  """
  game_session_configuration_id = StringField(primary_key=True,
                                              default=randomIdGenerator("GSC"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  game = ReferenceField(Game, required=True)
  specific_configuration = DictField()

  def toMinimalJson(self):
    return {
        "gameSessionConfigurationId": str(self.game_session_id),
        "gameId": str(self.game.game_id),
        "gameName": str(self.game.name),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "specificConfiguration": self.specific_configuration,
    })
    return json

  def __str__(self):
    return "(%(game_session_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
