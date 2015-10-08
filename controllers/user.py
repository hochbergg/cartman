from flask import Blueprint, jsonify, request, g

from models.login import Login
from models.cart import Cart
from services.auth.decorators import authorized_for


class UserController(Blueprint):
  """
  This controller responds to User API calls.

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
      return {"err": ("Cart '%s' not recognized" % cart_id), "code": 3}

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
      return {"err": ("Cart '%s' isn't assigned to user '%s'" % (cart_id, g.user.user_id)), "code": 2}

    cart = self._fetchCart(cart_id)
    if not cart:
      return {"err": ("Cart '%s' not recognized" % cart_id), "code": 3}

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

  def _fetchCart(self, cart_id):
    """
    Fetches cart by given ID.
    """
    try:
      return Cart.objects(cart_id=cart_id).get()
    except:
      return None


# Create and initialize the controller for serving the app files.
ctrl = UserController("user", __name__, static_folder="../public")

# User API paths.

@ctrl.route("/api/user/take_cart/", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def take_cart():
  res = ctrl.takeCart(request.get_json().get("cart_id"))
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