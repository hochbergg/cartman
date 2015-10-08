import datetime
from mongoengine import *

from lib.id_generator import randomIdGenerator


class Game(Document):
  """
  This model represents a Game in the database.

  It contains all of the configuration details, game file locations, and
  gathered statistics for a single game in the system.
  """
  game_id = StringField(primary_key=True,
                        default=randomIdGenerator("G"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  location = StringField(required=True)
  configuration = DictField()

  def toMinimalJson(self):
    return {
        "gameId": str(self.game_id),
        "name": str(self.name),
        "location": str(self.location),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "configuration": self.configuration,
    })
    return json

  def __str__(self):
    return "(%(game_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
