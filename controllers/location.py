import datetime

from flask import Blueprint, jsonify, request, g

from models.login import Login
from models.cart import Cart
from models.user import User
from services.auth.decorators import authorized_for


class LocationController(Blueprint):
  """
  This controller responds to Location API calls.

  the _fetch* methods are for fetching data from the database.
  """

  def nearbyCarts(self, cart_ids):
    """
    Updates state of given carts within range of current User.
    TODO push notifications in all mentioned places in private methods
    """
    user = g.user
    if not user:
      return {"err": "User not found", "code": 1}

    if user.enclosure:
      self._handleCartsNearEnclosure(user, cart_ids)
      self._handleComplementingCartsNearEnclosure(user, cart_ids)

    else:
      self._handleCartsNearSentinel(user, cart_ids)

    return {"msg": "OK"}

  def _handleCartsNearEnclosure(self, user, cart_ids):
    """
    Updates state of given carts within range of Enclosure.
    """
    for cart_id in cart_ids:
        cart = self._fetchCart(cart_id)

        if cart.rental_state == cart.RentalState.STOLEN or cart.rental_state == cart.RentalState.RENTED:
          cart.rental_state = cart.RentalState.WAITING
          cart.enclosed = True

          renting_user = self._fetchUser(cart.renting_user)
          renting_user.cart = None
          renting_user.save()

          cart.renting_user = None
          cart.renting_time = None

          if cart.rental_state == cart.RentalState.STOLEN:
            res_dict = {"msg": ("Cart '%s' has been returned! To user '%s' the spoils!" %
                                (cart.cart_id, cart.last_seen_by)), "code": 1}
          else:
            res_dict = {"msg": ("User '%s' return cart '%s'" %
                                (renting_user.user_id, cart.cart_id)), "code": 2}

        cart.state_last_updated = datetime.datetime.now()
        cart.last_seen_by = user
        cart.save()

        print res_dict # TODO - push notification

  def _handleComplementingCartsNearEnclosure(self, user, cart_ids):
    """
    Updates state of all carts other than given list, assuming given list is of carts within range of Enclosure.
    i.e. carts to be treated are ones not in Enclosure sight.
    """
    complementing_carts = self._fetchComplementingCarts(cart_ids)
    for cart in complementing_carts:
      if cart.rental_state == cart.RentalState.ASSIGNED_IN_ENCLOSURE:
        cart.rental_state = cart.RentalState.RENTED
        cart.enclosed = False

        renting_user = cart.last_seen_by
        renting_user.cart = cart
        renting_user.save()

        cart.renting_user = renting_user
        cart.renting_time = datetime.datetime.now()

        res_dict = {"msg": ("Cart '%s' has been rented to user '%s'" %
                              (cart.cart_id, cart.renting_user)), "code": 3}

      elif cart.rental_state == cart.RentalState.WAITING:
        cart.rental_state = cart.RentalState.STOLEN
        cart.enclosed = False

        res_dict = {"msg": ("Cart '%s' has been stolen! Thief's identity unknown :(" % cart.cart_id), "code": 4}

      elif cart.rental_state == cart.RentalState.RENTED:
        if cart.max_renting_time and cart.renting_time > cart.max_renting_time:
          cart.rental_state.STOLEN # TODO differentiate between message with little time left to time past

          res_dict = {"msg": ("Cart '%s' has been stolen! User '%s' - you BASTARD!" %
                              (cart.cart_id, cart.renting_user)), "code": 4}

      cart.state_last_updated = datetime.datetime.now()
      cart.last_seen_by = user
      cart.save()

      print res_dict # TODO - push notification

  def _handleCartsNearSentinel(self, user, cart_ids):
    """
    Updates state of given carts within range of Sentinel.
    """
    for cart_id in cart_ids:
      cart = self._fetchCart(cart_id)
      if cart.rental_state == cart.RentalState.STOLEN:
        res_dict = {"msg": ("User '%s' found stolen cart '%s'" % (user.user_id, cart.cart_id)), "code": 6}

        cart.state_last_updated = datetime.datetime.now()
        cart.last_seen_by = user
        cart.save()

        print res_dict # TODO - push notification

      elif cart.rental_state == cart.RentalState.WAITING:
        cart.rental_state = cart.RentalState.ASSIGNED_IN_ENCLOSURE
        res_dict = {"msg": ("Cart '%s' is now assigned to user '%s' and still in enclosure" %
                            (user.user_id, cart.cart_id)), "code": 7}

        cart.state_last_updated = datetime.datetime.now()
        cart.last_seen_by = user
        cart.save()

        print res_dict # TODO - push notification

  def _fetchCart(self, cart_id):
    """
    Fetches cart by given ID.
    """
    try:
      return Cart.objects(cart_id=cart_id).get()
    except:
      return None

  def _fetchUser(self, user_id):
    """
    Fetches user by given ID.
    """
    try:
      return User.objects(user_id=user_id).get()
    except:
      return None

  def _fetchComplementingCarts(self, cart_ids):
    """
    Fetches complementing carts to given cart_ids related to all carts in DB.
    """
    carts = [self._fetchCart(cart_id) for cart_id in cart_ids]
    all_carts = Cart.objects()
    return [cart for cart in all_carts if cart not in carts]

# Create and initialize the controller for serving the app files.
ctrl = LocationController("location", __name__, static_folder="../public")

# User API paths.

@ctrl.route("/api/location/nearby_carts", methods=["POST"])
@authorized_for(role=Login.Role.USER)
def nearby_carts():
  res = ctrl.nearbyCarts(request.get_json().get("cart_ids"))
  return jsonify(**res)
