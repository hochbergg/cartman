__author__ = 'shiriladelsky'

import datetime

from flufl.enum import Enum
from mongoengine import *
from lib.id_generator import randomIdGenerator


class Cart(Document):
  """
  This model represents a Cart in the database.
  """
  cart_id = StringField(primary_key=True,
                         default=randomIdGenerator("C"))

  creation_time = DateTimeField(default=datetime.datetime.now)

  renting_user = GenericReferenceField()
  renting_time = DateTimeField()
  max_renting_time = DateTimeField()

  class Status(Enum):
    CAGED = 0
    RENTED = 1
    STOLEN = 2
  
  def status(self):
    if not self.renting_user:
      return self.Status.CAGED
    if self.max_renting_time and self.renting_time > self.max_renting_time:
      return self.Status.STOLEN
    return self.status.RENTED

  def toMinimalJson(self):
    return {
        "cartId": str(self.cart_id),
        "userId": self.user.user_id if self.user else None,
        "status": str(self.status().name),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    return json

  def __str__(self):
    return "(%(cart_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
