import datetime
import time
import pytz
from tzlocal import get_localzone

def template_influx(measurement, timestamp, tags=None, fields=None):
    json_database_body = []
    json_database_message = {"measurement": measurement,
                             "time": timestamp,
                             "tags": tags,
                             "fields": fields}
    json_database_body.append(json_database_message)
    return json_database_body


def template_influx_status(apiStatus_bool):
    json_database_body = []
    fields = {
        "apiStatus_bool": bool(apiStatus_bool)
    }

    json_database_message = {"measurement": "logger",
                             "tags": {"type": "info"},
                             "fields": fields}
    json_database_body.append(json_database_message)
    return json_database_body
