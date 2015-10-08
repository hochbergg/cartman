import datetime
from mongoengine import *

from event import Event
from lib.id_generator import randomIdGenerator


class Symptom(Document):
  """
  This model represents a measurable Symptom from a game in the database.
  """
  symptom_id = StringField(primary_key=True,
                           default=randomIdGenerator("S"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  name = StringField(required=True)
  data = DictField()

  game_session = GenericReferenceField(required=True)
  events = ListField(ReferenceField(Event))

  def toMinimalJson(self):
    obj = self.to_mongo()
    return {
        "symptomId": str(self.symptom_id),
        "name": str(self.name),
        "gameSessionId": (str(obj["game_session"]["_ref"].id)
                          if "game_session" in obj else None),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "data": self.configuration,
        "events": [e.toMinimalJson() for e in self.events],
    })
    return json

  def __str__(self):
    return "(%(symptom_id)s) %(name)s" % self._data

  def __repr__(self):
    return self.__str__()
