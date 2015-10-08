import os

# Database settings.
MONGODB_SETTINGS = {
  "host": os.environ.get("MONGOLAB_URI", "localhost"),
}

# Web URL settings.
WEB_SHORT_DOMAIN = os.environ.get("WEB_SHORT_DOMAIN",
                                  "robo-feuerstein.herokuapp.com")
WEB_FULL_DOMAIN = os.environ.get("WEB_FULL_DOMAIN",
                                 "https://robo-feuerstein.herokuapp.com/")

# User authentication settings.
SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", os.urandom(24))
REMEMBER_COOKIE_NAME = "robofeuerstein"
REMEMBER_COOKIE_DOMAIN = "." + WEB_SHORT_DOMAIN
TOKEN_TIMEOUT = 30*24*60*60  # 1 month.
TOKEN_ROLE_SETTINGS = {
  "USER": {
    "COOKIE_TIMEOUT": 24*60*60,  # 1 day.
    "SESSION_TIMEOUT": 30*60,  # 30 minutes.
  },
  "CLIENT": {
    "COOKIE_TIMEOUT": 30*24*60*60,  # 1 month.
  },
  "ADMIN": {
    "COOKIE_TIMEOUT": 24*60*60,  # 1 day.
  },
}
