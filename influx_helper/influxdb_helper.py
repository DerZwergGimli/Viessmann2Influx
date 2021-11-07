import datetime
import logging
from contextlib import suppress
from time import timezone
import time

import PyViCare
import influxdb.exceptions
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from loguru import logger
from influxdb import InfluxDBClient

from influx_helper.influx_templates import json_influx_template_modular

internal_version = 0.1


class VMStoInflux:
    def init_connection(self, json_influx):
        # Connect to InfluxDB
        try:
            self.client_influx = InfluxDBClient(json_influx["address"],
                                                json_influx["port"],
                                                json_influx["user"],
                                                json_influx["password"],
                                                json_influx["database_name"])

            self.client_influx.create_database(json_influx["database_name"])
            return 0
        except Exception as e:
            logger.error(e.__str__())
            logger.error("Server is running and reachable?")
            return 1

    def write_viessmannDevice(self, vsm_vicare: PyViCare):
        logger.info("Starting writing to DB")
        tags = {"type": "viessmannDevice",
                #        "isEnabled":        data_point.get("isEnabled"),
                #        "isReady":          data_point.get("isReady"),
                #        "gatewayId":        data_point.get("gatewayId"),
                #        "apiVersion":       data_point.get("apiVersion"),
                "internal_version": internal_version
                }
        vsm_device = vsm_vicare.devices[0]
        measurement = "viessmann.Device.Info"

        self.write_infux_db(json_influx_template_modular(measurement, tags, {"Model": vsm_device.getModel()}))
        self.write_infux_db(json_influx_template_modular(measurement, tags, {"isOnline": vsm_device.isOnline()}))

        device = vsm_device.asAutoDetectDevice()
        self.write_infux_db(json_influx_template_modular(measurement, tags, {"auto-name": str(type(device).__name__)}))

        check = 0
        for idx, i in enumerate(vsm_vicare.installations):
            tags["index_installations"] = idx
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Installation-id": i.id}))
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Installation-description": i.description}))
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Installation-address": str(i.address.street)}))
        for idy, g in enumerate(i.gateways):
            tags["index_gateways"] = i
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Gateway-producedAt": str(g.producedAt)}))
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Gateway-autoUpdate": g.autoUpdate}))
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Gateway-aggregatedStatus": g.aggregatedStatus}))
            check += self.write_infux_db(
                json_influx_template_modular(measurement, tags, {"Gateway-registeredAt": str(g.registeredAt)}))
            for idz, d in enumerate(g.devices):
                tags["index_devices"] = idz
                check += self.write_infux_db(
                    json_influx_template_modular(measurement, tags, {"Devices-modelId": d.modelId}))
                check += self.write_infux_db(
                    json_influx_template_modular(measurement, tags, {"Devices-createdAt": d.modelId}))
        if check == 0:
            logger.info("Written '" + measurement + "' to Database")

    def make_inlfux_device(self, vsm_device):
        try:
            for idx, vsm_device_sub in enumerate(vsm_device):
                self.create_influx_device_message(vsm_device_sub, idx)
        except TypeError:
            self.create_influx_device_message(vsm_device)

    def create_influx_device_message(self, vsm_device_sub, idx=""):
        check = 0
        device_name = str((str(type(vsm_device_sub)).split("."))[-1:])[2:-4]
        function_list_getter = [method for method in dir(type(vsm_device_sub)) if
                                method.startswith('get') is True]
        for function in function_list_getter:
            method = getattr(vsm_device_sub, function)
            with suppress(PyViCareNotSupportedFeatureError):
                try:
                    measurement_name = "viessmann." + device_name + ".Data"
                    tags = {"type": "viessmannDevice", "internal_version": internal_version}

                    # Handle with care
                    data = self.convert_datatype(method())
                    if type(data) == list:
                        for idx, data_sub in enumerate(method()):
                            tags["index"] = idx
                            data_sub = self.convert_datatype(data_sub)
                            check += self.write_infux_db(
                                json_influx_template_modular(measurement_name + ".list", tags,
                                                             {str(function[3:]): data_sub}))
                    elif type(data) == dict:
                        # Special care for dict
                        for idx, data_sub in enumerate(method()):
                            # if only one value exists
                            if type(data[data_sub]) != list:
                                tags["index"] = idx
                                check += self.write_infux_db(
                                    json_influx_template_modular(measurement_name + ".dict",
                                                                 tags, {str(data_sub): method()[data_sub]}))
                            # if there are multiple entries
                            else:
                                # find inner elements of multiple
                                tags["parent"] = str(data_sub)
                                for idy, data_subsub in enumerate(method()[data_sub]):
                                    # find value and name of inner element
                                    tags["index"] = idy
                                    for idz, enity in enumerate(data_subsub):
                                        check += self.write_infux_db(
                                            json_influx_template_modular(measurement_name + ".dict",
                                                                         tags, {str(enity): data_subsub[enity]}))
                    else:
                        check += self.write_infux_db(
                            json_influx_template_modular(measurement_name, tags, {str(function[3:]): data}))
                except TypeError as e:
                    logger.warning("Type error - getting ignored:" + e.__str__())
        # Give some feedback
        if check == 0:
            logger.info("Written '" + measurement_name + "' to Database")
        else:
            logger.error("Not all data was written for " + measurement_name)

    def convert_datatype(self, data):
        dataype = type(data)
        if dataype == bool:
            return bool(data)
        elif dataype == int:
            return float(data)
        elif dataype == float:
            return float(data)
        elif dataype == list:
            return data
        elif dataype == str:
            return str(data)
        elif dataype == dict:
            return data
        else:
            raise TypeError("datatype error while converting:" + str(data))


    def write_infux_db(self, json_inlfux):
        try:
            self.client_influx.write_points(json_inlfux)
            return 0
        except Exception as e:
            logger.error("Error while writing to influxDB:" + e.__str__())
            return 1
