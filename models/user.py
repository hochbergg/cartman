import datetime

from mongoengine import *
from lib.id_generator import randomIdGenerator
from login import Login

from models.cart import Cart


class User(Document):
    """
    This model represents a User in the database.

    It contains all of the information we have on a specific user, along with
    profile information to be used by communication and collection algorithms.
    """
    user_id = StringField(primary_key=True,
                          default=randomIdGenerator("U"))

    login = ReferenceField(Login)

    creation_time = DateTimeField(default=datetime.datetime.now)

    cart = ReferenceField(Cart)

    enclosure = BooleanField(default=False)

    notifications = ListField(DictField())

    def username(self):
      if not self.login:
        return None
      return self.login.username

    def toMinimalJson(self):
        return {
            "userId": str(self.user_id),
            "username": str(self.login.username) if self.login else None,
            "authenticated": (bool(self.login.authenticated)
                              if self.login and self.login.authenticated else None),
            "cartId": self.cart.cart_id if self.cart else None
        }

    def toFullJson(self):
        return self.toMinimalJson()

    def __str__(self):
        return "(%(user_id)s)" % self._data

    def __repr__(self):
        return self.__str__()
