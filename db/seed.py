from datetime import datetime, timedelta
from dateutil.relativedelta import *
from flask import (Flask, request, session, g, redirect, url_for,
                   abort, render_template, flash, jsonify, Response)
from flask.ext.mongoengine import MongoEngine
import hashlib
import math
import os
from urllib import urlopen
from random import randint

from services.auth.login_service import login_service
from lib.configure import configure_app
from models.all import *


def seed_users():
  User.drop_collection()
  Login.drop_collection()

  for i, user_domain in enumerate(["t", "r"]):
    # Nadir's User.
    user1 = User(user_id="U00000000001111" + str(i), active=True)
    user1.login = Login(
            username=(user_domain + "nadir"),
            password_hash=login_service._getHashedPassword(user_domain + "nadir"),
            urole=Login.Role.USER,
            active=True)
    user1.login.save()
    user1.save()
    user1.login.user = user1
    user1.login.save()

    # Ori's User.
    user2 = User(user_id="U00000000001112" + str(i), active=True)
    user2.login = Login(
            username=(user_domain + "ori"),
            password_hash=login_service._getHashedPassword(user_domain + "ori"),
            urole=Login.Role.USER,
            active=True)
    user2.login.save()
    user2.save()
    user2.login.user = user2
    user2.login.save()

    # Shaked's User.
    user3 = User(user_id="U00000000001113" + str(i), active=True)
    user3.login = Login(
            username=(user_domain + "shaked"),
            password_hash=login_service._getHashedPassword(user_domain + "shaked"),
            urole=Login.Role.USER,
            active=True)
    user3.login.save()
    user3.save()
    user3.login.user = user3
    user3.login.save()

def seed_admins():
  Admin.drop_collection()

  # Our Admin.
  user1 = Admin(admin_id="ADMIN00000000001", active=True)
  user1.login = Login(
          username="admin",
          password_hash=login_service._getHashedPassword("Password1"),
          urole=Login.Role.ADMIN,
          active=True)
  user1.login.save()
  user1.save()
  user1.login.user = user1
  user1.login.save()

def seed_carts():
  Cart.drop_collection()

  for i in range(10):
    cart = Cart(cart_id=("C00000000000000%s" % i))
    cart.save()

def seed_all():
  print "Seeding DB..."
  seed_users()
  seed_admins()
  seed_carts()
  print "Done."


if __name__ == "__main__":
  # Create and initialize the app.
  app = Flask(__name__, static_folder="public")
  db = MongoEngine()
  configure_app(app, db, login_service)

  # Seed the DB.
  seed_all()
