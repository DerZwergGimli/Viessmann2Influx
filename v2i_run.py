# Externals
import requests.exceptions
from PyViCare.PyViCare import PyViCare
from loguru import logger

# Internals
import file_helper.file_helper as fileHelper
from influx_helper.influxdb_helper import VMStoInflux

credentialsFilePath = "./conf/conf.json"

if __name__ == '__main__':
    logger.add("log_file.log",
               rotation="10 MB",
               colorize=True,
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    logger.info("Started...")

    j_config = fileHelper.read_file_to_json(credentialsFilePath)

    db_credentials = j_config["influxdb"]
    adapter = VMStoInflux()
    db_status = adapter.init_connection(db_credentials)

    if db_status == 1:
        logger.info("Quitting... There is no DB connection nothing to do!")
        exit()

    vicare = PyViCare()
    try:
        v_credentials = j_config["viessmannapi"]
        vicare.initWithCredentials(v_credentials["email"], v_credentials["password"], v_credentials["api_key"],
                                   "token.save")
        adapter.write_viessmannDevice(vicare)

        if vicare.devices[0].isOnline():
            for idx, device in enumerate(vicare.devices):
                # Device
                device = vicare.devices[idx].asAutoDetectDevice()
                #printALL(device)
                adapter.make_inlfux_device(device)

                # Circuits
                #printALL(device.circuits)
                adapter.make_inlfux_device(device.circuits)

                # Burner
                #printALL(device.burners)
                adapter.make_inlfux_device(device.burners)

                # Compressor
                #printALL(device.compressors)
                adapter.make_inlfux_device(device.compressors)


    except requests.exceptions.ConnectionError:
        logger.error("Unable to connect to API - check internet connection")

    logger.info("...Finished")

