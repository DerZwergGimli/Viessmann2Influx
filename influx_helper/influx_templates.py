def json_influx_template_modular(measurement: str, time, tags: {}, fields: {}):
    json_database_body = []
    json_inner_message = {"measurement": measurement, "time": time, "tags": tags, "fields": fields}

    json_database_body.append(json_inner_message)
    #print(json_database_body)
    return json_database_body

def json_influx_template_modular(measurement: str, tags: {}, fields: {}):
    json_database_body = []
    json_inner_message = {"measurement": measurement, "tags": tags, "fields": fields}

    json_database_body.append(json_inner_message)
    #print(json_database_body)
    return json_database_body
