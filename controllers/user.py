import itertools
import os

from dateutil.parser import parse
from flask import Blueprint, jsonify, request, g, abort
from mongoengine import Q
from models.login import Login
from models.user import User
from models.cart import Cart
from services.auth.decorators import authorized_for, update_login_access
from services.auth.login_service import login_service


class UserController(Blueprint):
  """
  This controller responds to User API calls.

  The get* methods are for returning data for the corresponding API calls.
  the _fetch* methods are for fetching data from the database.
  """

  def takeCart(self, cart_id):
    """
    Assigns given cart to current User.
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}

    if user.cart:
      return {"err": "User already has a cart", "code": 2}

    cart = self._fetchCart(cart_id)
    if not cart:
      return {"err": ("Cart '%s' not recognized", cart_id), "code": 3}

    user.cart = cart
    user.save()
    cart.user = user
    cart.save()

    return {"msg": "OK"}

  def returnCart(self, cart_id):
    """
    Unassigns given cart from current User.
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}

    if user.cart.cart_id != cart_id:
      return {"err": ("Cart '%s' isn't assigned to user '%s", cart_id, g.user.user_id), 2}

    cart = self._fetchCart(cart_id)
    if not cart:
      return {"err": ("Cart '%s' not recognized", cart_id), "code": 3}

    user.cart = None
    user.save()
    cart.user = None
    cart.save()

    return {"msg": "OK"}

  def submitFoundCart(self, cart_id):
    """
    Submits found cart by current User.
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}
    return {"msg": "OK"}



  def getUserInfo(self):
    """
    Returns the User info for the currently logged in User.
    """
    user = g.user
    if not user:
      return None

    json = user.toFullJson()

    return json

  def startNewUserSession(self, user):
    """
    Starts a new UserSession for the given User.
    """
    # Fetch the relevant UserSessionConfiguration.
    session_configuration = self._fetchUserSessionConfigurationForUser(user)

    # Create the new Session.
    session = UserSession(user=user,
                          user_session_configuration=session_configuration)
    session.save()

    # Set it as the current session for the User.
    user.set_session(session)
    user.save()

  def getUserGameLocation(self):
    """
    Returns the location of the current game for the User.
    """
    user = g.user
    if not user:
      return None

    user_session = user.current_session
    if not user_session:
      return None

    game_session = user_session.current_game_session()
    if not game_session or not game_session.running:
      game_session = self._createGameSession(user_session)

    return game_session.game.location

  def _fetchCart(self, cart_id):
    try:
      return Cart.objects(cart_id=cart_id).get()
    except:
      return None

  def _fetchUserSessionConfigurationForUser(self, user):
    if user.user_session_configuration:
      return user.user_session_configuration
    try:
      return UserSessionConfiguration.objects(name="default").get()
    except:
      return None

  def _createGameSession(self, user_session):
    next_config = user_session.next_game_session_configuration()
    # if not next_config:
    #   return None

    game_session = GameSession(game=next_config.game,
                               game_session_configuration=next_config)
    game_session.save()

    user_session.game_sessions.append(game_session)
    user_session.save()

    return game_session

# Create and initialize the controller for serving the app files.
ctrl = UserController("user", __name__, static_folder="../public")

# User API paths.

@ctrl.route("/api/user/take_cart/", methods=["POST"])
def take_cart():
  res = ctrl.takeCart(request.get_json().get("cart_id"))
  return jsonify(**res)

@ctrl.route("/api/user/return_cart/", methods=["POST"])
def return_cart():
  res = ctrl.returnCart(request.get_json().get("cart_id"))
  return jsonify(**res)


@ctrl.route("/api/user/submit_found_cart/", methods=["POST"])
def submit_found_cart():
  res = ctrl.submitFoundCart(request.get_json().get("cart_id"))
  return jsonify(**res)


# Old controller API paths
@ctrl.route("/api/user/info/")
@authorized_for(role=Login.Role.USER)
@update_login_access
def get_user_info():
  info = ctrl.getUserInfo()
  if not info:
    return jsonify(err=("No user found for ID: '%s'" %
                        (g.user.user_id if g.user else None)))
  return jsonify(info=info)

@ctrl.route("/api/user/games/current_game/")
@authorized_for(role=Login.Role.USER)
@update_login_access
def user_game_root():
  # game = ctrl.getUserGameLocation()
  game = "common/games/nback-5"
  if not game:
    return abort(404)
  return ctrl.send_static_file(os.path.join(game, "index.html"))

# Game paths.
@ctrl.route("/api/user/games/current_game/<path:path>")
@authorized_for(role=Login.Role.USER)
def user_game_proxy(path):
  # game = ctrl.getUserGameLocation()
  game = "common/games/nback-5"
  if not game:
    return abort(404)
  return ctrl.send_static_file(os.path.join(game, path))

# TODO: Remove this when we fix this issue.
@ctrl.route("/api/user/games/<path:path>")
@authorized_for(role=Login.Role.USER)
def user_games_main_dir_proxy(path):
  return ctrl.send_static_file(os.path.join("common", "games", path))

# TODO: Remove this.
@ctrl.route("/api/user/games/trivia_game/")
@authorized_for(role=Login.Role.USER)
@update_login_access
def trivia_game_root():
  # game = ctrl.getUserGameLocation()
  game = "common/games/trivia"
  if not game:
    return abort(404)
  return ctrl.send_static_file(os.path.join(game, "index.html"))

# TODO: Remove this.
@ctrl.route("/api/user/games/trivia_game/<path:path>")
@authorized_for(role=Login.Role.USER)
def trivia_game_proxy(path):
  # game = ctrl.getUserGameLocation()
  game = "common/games/trivia"
  if not game:
    return abort(404)
  return ctrl.send_static_file(os.path.join(game, path))