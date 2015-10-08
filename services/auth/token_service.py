from itsdangerous import URLSafeTimedSerializer


class TokenService:
  """
  Handles the creation and verification of tokens for the Login class.
  """
  def configure(self, config):
    """
    Configures the various timeout for tokens, and initialize the serializer.
    """
    # Import configuration parameters for tokens.
    self.token_timeout = config.get("TOKEN_TIMEOUT")

    # Initialize the serializer with its underlying encryption.
    self.serializer = URLSafeTimedSerializer(config.get("SECRET_KEY"))

  def generateToken(self, login):
    """
    Generates a token for the given Login instance, returning the serialized
    encrypted string.
    """
    data = (login.username, login.password_hash)
    return self.serializer.dumps(data)

  def loadToken(self, token_data, timeout=None):
    """
    Loads the token from the given serialized token data, returning the internal
    data from it (or None if an unauthorized access occurs.
    """
    # Max age in seconds is determined by the configuration, and if not
    # specifically set in the global settings, is ignored.
    extra_params = {}
    if timeout:
      extra_params["max_age"] = int(timeout)
    elif self.token_timeout:
      extra_params["max_age"] = int(self.token_timeout)

    # Deserialize the token data and if an error occurs return None.
    try:
      return self.serializer.loads(token_data, **extra_params)
    except Exception, e:
      print "ERROR: TokenService.loadToken failed to deserialize token: %s" % e
      return None

token_service = TokenService()
