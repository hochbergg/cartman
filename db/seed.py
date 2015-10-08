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

  for i, user_domain in enumerate(["t", "r"]):
    # Nadir's User.
    user1 = User(user_id="U00000000001111" + str(i), active=True)
    user1.personal_info = PersonalInfo(first_name="Nadir",
                                       last_name="Izrael")
    user1.contact_infos = [ContactInfo(name="Nadir Izrael",
                                       email="nadir.izr@gmail.com",
                                       phone_number="+972-54-9454091")]
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
    user2.personal_info = PersonalInfo(first_name="Ori",
                                       last_name="Birnboim")
    user2.contact_infos = [ContactInfo(name="Ori Birnboim",
                                       email="oribirnboim@me.com",
                                       phone_number="+972-54-4682455")]
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
    user3.personal_info = PersonalInfo(first_name="Shaked",
                                       last_name="Gitelman")
    user3.contact_infos = [ContactInfo(name="Shaked Gitelman",
                                       email="shaked.gitelman@gmail.com",
                                       phone_number="+972-54-7449102")]
    user3.login = Login(
            username=(user_domain + "shaked"),
            password_hash=login_service._getHashedPassword(user_domain + "shaked"),
            urole=Login.Role.USER,
            active=True)
    user3.login.save()
    user3.save()
    user3.login.user = user3
    user3.login.save()

def seed_all():
  print "Seeding DB..."
  seed_users()
  print "Done."


if __name__ == "__main__":
  # Create and initialize the app.
  app = Flask(__name__, static_folder="public")
  db = MongoEngine()
  configure_app(app, db, login_service)

  # Seed the DB.
  seed_all()
