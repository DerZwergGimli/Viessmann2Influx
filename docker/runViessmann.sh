#!/bin/bash
echo "Staring fetching Viessmann API..." >> /proc/1/fd/1
cd /home/python/Viessmann_API_InfluxDB_Logger && python3 python_viessmannapi.py >> /dev/null
echo "...Fetched Viessmann API!" >> /proc/1/fd/1