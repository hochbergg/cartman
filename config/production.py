import os

# Database settings.
MONGODB_SETTINGS = {
  "host": os.environ.get("MONGOLAB_URI", "localhost"),
}

# Web URL settings.
WEB_SHORT_DOMAIN = os.environ.get("WEB_SHORT_DOMAIN",
                                  "cartman-server.herokuapp.com")
WEB_FULL_DOMAIN = os.environ.get("WEB_FULL_DOMAIN",
                                 "https://cartman-server.herokuapp.com/")

# User authentication settings.
SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", os.urandom(24))
REMEMBER_COOKIE_NAME = "cartman"
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


# PayPal Configuration - this is still SandBox

PAYPAL_CLIENT_ID = 'AcfRZqmrrgJLrIemcJLSkBuSKEzDDgwEhgb-B29qi5irgm6hgXssH5-9V6M05vj2MBIHPASHDcRMHLNv'
PAYPAL_SECRET = 'ELdGaLLdSrKvNC-OANdOYfJmwqSMfYQU1Tawh1DAdMka11qFJLQq4HEm9DjtIhTDRDgQ4EGWD_I1dFQD'
PAYPAL_ENDPOINT = 'api.sandbox.paypal.com'
