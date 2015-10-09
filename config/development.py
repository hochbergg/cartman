DEBUG = True

# Database settings.
MONGODB_SETTINGS = {
    "db": "heroku_nf6dqdm4",
    "host": "mongodb://heroku_nf6dqdm4:mvgb4g2erhkmbd36ua98u1hmmq@ds033734.mongolab.com:33734/heroku_nf6dqdm4"
}

# Web URL settings.
WEB_SHORT_DOMAIN = "localhost:5000"
WEB_FULL_DOMAIN = "http://localhost/"

# User authentication settings.
SECRET_KEY = "I'M A SECRET KEY! REALLY!!"
REMEMBER_COOKIE_NAME = "cartman"
REMEMBER_COOKIE_DOMAIN = "." + WEB_SHORT_DOMAIN
TOKEN_TIMEOUT = 30 * 24 * 60 * 60  # 1 month.
TOKEN_ROLE_SETTINGS = {
    "USER": {
        "COOKIE_TIMEOUT": 24 * 60 * 60,  # 1 day.
        "SESSION_TIMEOUT": 30 * 60,  # 30 minutes.
    },
}

# Cart renting settings.
MAX_RENTING_DURATION = 60  # 60 seconds.
FINE_AMOUNT = 1  # 1$.


# PayPal Configuration

PAYPAL_CLIENT_ID = 'AcfRZqmrrgJLrIemcJLSkBuSKEzDDgwEhgb-B29qi5irgm6hgXssH5-9V6M05vj2MBIHPASHDcRMHLNv'
PAYPAL_SECRET = 'ELdGaLLdSrKvNC-OANdOYfJmwqSMfYQU1Tawh1DAdMka11qFJLQq4HEm9DjtIhTDRDgQ4EGWD_I1dFQD'
PAYPAL_ENDPOINT = 'api.sandbox.paypal.com'
