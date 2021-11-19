import influxdb.exceptions
from influxdb import InfluxDBClient
from loguru import logger

class DatabaseAdapter:
    def connect(self, json_influx):
        try:
            self.client_influx = InfluxDBClient(json_influx["address"],
                                                json_influx["port"],
                                                json_influx["user"],
                                                json_influx["password"],
                                                json_influx["database_name"])

            self.client_influx.create_database(json_influx["database_name"])
            logger.info("Connected to DB!")
            return 0
        except Exception as e:
            logger.error(e.__str__())
            logger.error("Unable to connect to DB!")
            return 1

    def write(self, json_message):
        try:
            status = self.client_influx.write_points(json_message)
            if not status:
                logger.warning("DB writing returned:" + str(status))
        except influxdb.exceptions.InfluxDBClientError as e:
            logger.error(e.__str__())
            logger.warning("Unable to write:" + str(json_message))
