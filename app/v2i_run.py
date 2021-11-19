import getopt
import sys
import time
from tqdm import tqdm

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareUtils import PyViCareInternalServerError
from loguru import logger

from database.DatabaseAdapter import DatabaseAdapter
from database.DatabaseTemplate import template_influx, template_influx_status
from file_helper.file_helper import read_file_to_json
credentialsFilePath = "./conf/conf.json"


def casting(value, data_type):
    if data_type == "number":
        return float(value)
    elif data_type == "boolean":
        return bool(value)
    else:
        return str(value)


def run():
    j_config = read_file_to_json(credentialsFilePath)
    v_credentials = j_config["viessmannapi"]

    database = DatabaseAdapter()
    if database.connect(j_config["influxdb"]) != 0:
        logger.info("No connection to DB - doesnt make sense to fetch anything! program will close now...")
        exit()

    apiStatus_bool = False
    try:
        vicare = PyViCare()
        vicare.initWithCredentials(v_credentials["email"], v_credentials["password"], v_credentials["api_key"],
                                   "token.save")
        apiStatus_bool = True
        database.write(template_influx_status(apiStatus_bool))
    except PyViCareInternalServerError as e:
        logger.error("Error connecting..." + e.__str__())
        logger.info("No connection to Viessmann - doesnt make sense to continue! program will close now...")
        database.write(template_influx_status(apiStatus_bool))
        #exit()

    for device in vicare.devices:
        for entry in device.get_raw_json()["data"]:
            print(entry)
            if entry.get("properties", {}):
                feature_parent = '.'.join(entry["feature"].split(".")[:2])
                feature_branch = '.'.join(entry["feature"].split(".")[2:3])
                feature_child = '.'.join(entry["feature"].split(".")[3:])
                tags = {
                    "feature": entry["feature"],
                    "feature_parent": feature_parent,
                    "feature_child": feature_child,
                    "feature_branch": feature_branch,
                    "apiVersion": entry["apiVersion"],
                    "uri": entry["uri"],
                    "gatewayId": entry["gatewayId"],
                    "isEnabled": entry["isEnabled"],
                    "isReady": entry["isReady"],
                    "deviceId": entry["deviceId"]
                }

                properties = entry.get("properties", {})

                for entity in properties.items():
                    tags["entity"] = str(entity[0])
                    fields = {}
                    data = entity[1]

                    # Find the type
                    data_type = ""
                    for point in data.items():
                        if str(point[0]).__contains__("type"):
                            data_type = point[1]

                    # Find the value to cast by defined type (above)
                    for point in data.items():
                        if str(point[0]).__contains__("value"):
                            if data_type.__contains__("array"):
                                for idx, item in enumerate(point[1]):
                                    # Handle array special
                                    tags["array_index"] = 100 + idx
                                    if str(item).replace('.', '', 1).isdigit():
                                        fields[str(point[0]) + "_array" + ".idx"] = casting(item, "number")
                                    else:
                                        fields[str(point[0]) + "_array" + ".idx"] = casting(item, "text")
                                    database.write(template_influx(measurement=feature_parent,
                                                                   timestamp=entry["timestamp"],
                                                                   tags=tags,
                                                                   fields=fields))
                            else:
                                fields[str(point[0]) + "_" + str(data_type)] = casting(point[1], data_type)
                        else:
                            fields[str(point[0])] = str(point[1])
                    # Write DB
                    message = template_influx(measurement=feature_parent,
                                              timestamp=entry["timestamp"],
                                              tags=tags,
                                              fields=fields)
                    print(message)
                    database.write(message)


def arguments(argv):
    try:
        opts, args = getopt.getopt(argv, "hrs:", ["rmode=", "stime="])
    except getopt.GetoptError:
        print('v2i_run.py -h')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Help: (v2i_run.py):')
            print('v2i_run.py -r \t\t[to run normaly]')
            print('v2i_run.py -s 10 \t[to run without user interaction - time based (seconds)]')
            print('v2i_run.py \t\t[to run with normaly]')
            sys.exit()
        elif opt in ("-r", "--mode"):
            run()
            logger.info("{SingleRun} Done bye...!")
            quit()
        elif opt in ("-s", "--time"):
            print("Running in sleep mode: [auto]")
            sleep_time = arg
            print("sleep_time=" + str(sleep_time))

            while True:
                run()
                with tqdm(total=int(sleep_time)) as pbar:
                    for i in range(int(sleep_time)):
                        time.sleep(1)
                        pbar.update(1)
            quit()
    quit()

if __name__ == '__main__':
    logger.add("log_file.log",
               rotation="10 MB",
               colorize=True,
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    logger.info("Started...")

    arguments(sys.argv[1:])

