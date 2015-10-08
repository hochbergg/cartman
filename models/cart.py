__author__ = 'shiriladelsky'

import datetime

from mongoengine import *
from lib.id_generator import randomIdGenerator


class Cart(Document):
  """
  This model represents a Cart in the database.
  """
  cart_id = StringField(primary_key=True,
                         default=randomIdGenerator("C"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  user = GenericReferenceField()

  def toMinimalJson(self):
    obj = self.to_mongo()
    return {
        "cartId": str(self.cart_id),
        "userId": self.user.user_id if self.user else None
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    json.update({
        "data": self.configuration,
    })
    return json

  def __str__(self):
    return "(%(cart_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
