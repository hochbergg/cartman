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
  enclosed = BooleanField()
  rental_state = IntField()
  state_last_updated = DateTimeField()
  last_seen_by = GenericReferenceField()

  class RentalState(Enum):
    WAITING = 0
    ASSIGNED_IN_ENCLOSURE = 1
    RENTED = 2
    STOLEN = 3

  def toMinimalJson(self):
    return {
        "cartId": str(self.cart_id),
        "userId": self.renting_user.user_id if self.renting_user else None,
        "status": str(self.RentalState(self.rental_state).name),
      }

  def toFullJson(self):
    json = self.toMinimalJson()
    return json

  def __str__(self):
    return "(%(cart_id)s)" % self._data

  def __repr__(self):
    return self.__str__()
