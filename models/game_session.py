import datetime
from mongoengine import *

from event import Event
from game import Game
from game_session_configuration import GameSessionConfiguration
from symptom import Symptom
from lib.id_generator import randomIdGenerator


class GameSession(Document):
  """
  This model represents a session of a Game in the database.

  It contains all of the data, events, markers and interruptions of the game.
  """
  game_session_id = StringField(primary_key=True,
                                default=randomIdGenerator("GS"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  game = ReferenceField(Game, required=True)
  game_session_configuration = ReferenceField(GameSessionConfiguration)

  events = ListField(ReferenceField(Event))
  symptoms = ListField(ReferenceField(Symptom))



  running = BooleanField(default=True)

  def toMinimalJson(self):
    return {
        "gameSessionId": str(self.game_session_id),
        "gameId": str(self.game.game_id),
        "gameName": str(self.game.name),
        "gameSessionConfigurationId": (
            str(self.game_session_configuration.game_session_configuration_id)
            if self.game_session_configuration else None),
        "running": bool(self.running),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "events": [e.toMinimalJson() for e in self.events],
        "symptoms": [s.toMinimalJson() for s in self.symptoms],
    })
    return json

  def __str__(self):
    return "(%(game_session_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
