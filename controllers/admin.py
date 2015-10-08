import os
from datetime import datetime, timedelta

from flask import Blueprint, current_app, g, redirect, abort, jsonify, send_from_directory, request

from models.event import Event
from models.cart import Cart

from controllers.user import UserController
from models.login import Login
from services.auth.decorators import authorized_for

TIME_UNIT = 'minutes'
TIME_MEASUREMENT = 4


class AdminController(Blueprint):
    pass


ctrl = AdminController("admin", __name__,
                       static_folder=os.path.join(os.getcwd(), "public"))


@ctrl.route("/admin/log/data/")
def activity_log():
    event = Event(name='bla')
    event.save()
    events = Event.objects(
        creation_time__gte=(datetime.now() -
                            timedelta(TIME_UNIT=TIME_MEASUREMENT)))
    return jsonify(title='events from the last {} {}'.format(
                       TIME_MEASUREMENT, TIME_UNIT),
                   msg=[event.toMinimalJson() for event in events])


@ctrl.route("/admin/")
def admin_base():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_base.html')


@ctrl.route("/admin/log/")
def admin_log_view():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_log.html')


@ctrl.route("/admin/state/")
def admin_current_state_view():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_current_state.html')


@ctrl.route("/api/admin/user/token/")
@authorized_for(role=Login.Role.ADMIN)
def admin_get_user_token():
    user_id = request.values.get("user_id")
    try:
        user = User.objects(user_id=user_id).get()
        return jsonify(access_token=user.login.get_auth_token())
    except:
        return jsonify(err="User not found")


@ctrl.route("/api/admin/state/data/")
@authorized_for(role=Login.Role.ADMIN)
def current_state_of_carts():
    carts = Cart.objects()
    return jsonify(title='As of {}'.format(datetime.now()),
                   msg=[cart.toMinimalJson() for cart in carts])


@ctrl.route("/api/admin/change-status/", methods=['POST'])
@authorized_for(role=Login.Role.ADMIN)
def change_cart_status():
    request_data = request.get_json()
    # returnCart(cart_id=request_data.get('cartId'))
    return jsonify(msg='success')
