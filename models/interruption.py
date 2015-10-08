import datetime
from mongoengine import *

from marker import Marker
from lib.id_generator import randomIdGenerator


class Interruption(Document):
  """
  This model represents an Interruption in a game in the database.
  """
  interruption_id = StringField(primary_key=True,
                                default=randomIdGenerator("I"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  data = DictField()

  game_session = GenericReferenceField(required=True)
  markers = ListField(ReferenceField(Marker))

  def toMinimalJson(self):
    obj = self.to_mongo()
    return {
        "interruptionId": str(self.interruption_id),
        "name": str(self.name),
        "gameSessionId": (str(obj["game_session"]["_ref"].id)
                          if "game_session" in obj else None),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "data": self.configuration,
        "markers": [m.toMinimalJson() for m in self.markers],
    })
    return json

  def __str__(self):
    return "(%(marker_id)s) %(name)s" % self._data

  def __repr__(self):
    return self.__str__()
