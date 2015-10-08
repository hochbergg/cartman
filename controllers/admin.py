import os
from flask import Blueprint, current_app, g, redirect, abort, jsonify, send_from_directory
from models.event import Event
from models.cart import Cart
from datetime import datetime, timedelta

TIME_UNIT = 'minutes'
TIME_MEASUREMENT = 4


class AdminController(Blueprint):
    pass


ctrl = AdminController("admin", __name__, static_folder=os.path.join(os.getcwd(), "public"))


@ctrl.route("/admin/log/data/")
def activity_log():
    event = Event(name='bla')
    event.save()
    events = Event.objects(creation_time__gte=datetime.now() - timedelta(**{TIME_UNIT: TIME_MEASUREMENT}))
    return jsonify(title='events from the last {} {}'.format(TIME_MEASUREMENT, TIME_UNIT),
                   msg=[event.toMinimalJson() for event in events])


@ctrl.route('/admin/')
def admin_base():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_base.html')


@ctrl.route('/admin/log/')
def admin_log_view():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_log.html')


@ctrl.route('/admin/state/')
def admin_current_state_view():
    file_path_directory = os.path.join(ctrl.static_folder, "admin")
    return send_from_directory(file_path_directory, 'admin_current_state.html')


@ctrl.route("/admin/state/data/")
def current_state_of_carts():
    carts = Cart.objects()
    return jsonify(title='As of {}'.format(datetime.now()), msg=[cart.toMinimalJson() for cart in carts])

