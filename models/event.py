import datetime
from mongoengine import *

from lib.id_generator import randomIdGenerator


class Event(Document):
  """
  This model represents an Event from a game in the database.
  """
  event_id = StringField(primary_key=True,
                         default=randomIdGenerator("E"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  data = DictField()

  # game_session = GenericReferenceField(required=True)

  def toMinimalJson(self):
    obj = self.to_mongo()
    return {
        "eventId": str(self.event_id),
        "name": str(self.name),
        # "gameSessionId": (str(obj["game_session"]["_ref"].id)
        #                   if "game_session" in obj else None),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "data": self.configuration,
    })
    return json

  def __str__(self):
    return "(%(event_id)s) %(name)s" % self._data

  def __repr__(self):
    return self.__str__()
