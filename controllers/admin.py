from flask import Blueprint, current_app, g, redirect, abort, jsonify
from models.event import Event
from datetime import datetime, timedelta

TIME_UNIT = 'seconds'
TIME_MEASUREMENT = 4



class AdminController(Blueprint):
    pass


ctrl = AdminController("admin", __name__, static_folder="../public")


@ctrl.route("/admin/log/")
def activity_log():
    event = Event(name='bla')
    event.save()
    events = Event.objects(creation_time__gte=datetime.now() - timedelta(**{TIME_UNIT: TIME_MEASUREMENT}))
    return jsonify(title='events from the last {} {}'.format(TIME_MEASUREMENT, TIME_UNIT), msg=[event.toMinimalJson() for event in events])
