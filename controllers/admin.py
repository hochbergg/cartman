from flask import Blueprint, current_app, g, redirect, abort, jsonify
from models.event import Event

class AdminController(Blueprint):
    pass


ctrl = AdminController("admin", __name__, static_folder="../public")


@ctrl.route("/admin/log/")
def activity_log():
    event = Event(name='bla')
    event.save()
    events = Event.objects()
    return jsonify(msg=[event.toMinimalJson() for event in events])
