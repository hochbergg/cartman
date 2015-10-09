import datetime
from flask import Blueprint, jsonify, request, g

from models.login import Login
from models.cart import Cart
from services.auth.decorators import authorized_for


class UserController(Blueprint):
  """
  This controller responds to User API calls.

  the _fetch* methods are for fetching data from the database.
  """
  def register(self, app, options, first_registration=False):
    """
    Called when Blueprint is registered with the app on load.
    """
    self.max_renting_duration = app.config.get("MAX_RENTING_DURATION")

    super(UserController,
          self).register(app, options, first_registration)

  def takeCart(self, cart_id, username):
    """
    Assigns given cart to current User.
    """
    # user = g.user
    # if not user:
    #   return {"err": "User not found", "code": 1}

    login = Login.objects(username=username).get()
    user = login.user

    if user.cart:
      return {"err": "User already has a cart", "code": 2}

    cart = self._fetchCart(cart_id)
    if not cart:
      return {"err": ("Cart '%s' not recognized" % cart_id), "code": 3}

    user.cart = cart
    user.save()
    cart.renting_user = user
    cart.renting_time = datetime.datetime.now()
    cart.max_renting_time = ((cart.renting_time + datetime.timedelta(hours=6))
                             if self.max_renting_duration else None)
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
      return {"err": ("Cart '%s' isn't assigned to user '%s'" % (cart_id, g.user.user_id)), "code": 2}

    cart = self._fetchCart(cart_id)
    if not cart:
      return {"err": ("Cart '%s' not recognized" % cart_id), "code": 3}

    user.cart = None
    user.save()
    cart.renting_user = None
    cart.renting_time = None
    cart.max_renting_time = None
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

  def getPullNotifications(self):
    """
    Fetches all of the notifications for the User, and clears them.
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}
    
    notifications = [dict(n) for n in user.notifications]
    user.notifications.clear()
    user.save()

    return {"notifications": notifications}

  def postPullNotification(self, notification):
    """
    Add a push notification to the User queue.
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}

    user.notifications.append(notification)
    user.save()
    
    return { "msg": "OK" }

  def _fetchCart(self, cart_id):
    """
    Fetches cart by given ID.
    """
    try:
      return Cart.objects(cart_id=str(cart_id)).get()
    except:
      return None


# Create and initialize the controller for serving the app files.
ctrl = UserController("user", __name__, static_folder="../public")

# User API paths.

@ctrl.route("/api/user/take_cart/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def take_cart():
  res = ctrl.takeCart(request.get_json().get("cart_id"), "")
  return jsonify(**res)

@ctrl.route("/api/user/return_cart/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def return_cart():
  res = ctrl.returnCart(request.get_json().get("cart_id"))
  return jsonify(**res)

@ctrl.route("/api/user/submit_found_cart/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def submit_found_cart():
  res = ctrl.submitFoundCart(request.get_json().get("cart_id"))
  return jsonify(**res)

@ctrl.route("/api/user/notifications/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def pull_notifications():
  res = ctrl.getPullNotifications()
  return jsonify(**res)

@ctrl.route("/api/user/push_notification/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def push_notifications():
  res = ctrl.postPullNotification(request.get_json().get("notification"))
  return jsonify(**res)
