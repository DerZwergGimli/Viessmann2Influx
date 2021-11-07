# Cretae a telegraf container containing python and later install own application
FROM ubuntu
ENV TZ Europe/Berlin
RUN apt-get update 
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y && apt-get install -y python3 python3-pip cron nano

#Just some feedback about the version
RUN python3 -V
RUN pip3 -V

# SETUP CRON
ADD ../Viessmann2Influx /home/python/Viessmann2Influx
RUN pip3 install -r /home/python/Viessmann2Influx/requirements.txt

# Add files
ADD runViessmann.sh /runViessmann.sh
ADD watchdog.sh /watchdog.sh
ADD entrypoint.sh /entrypoint.sh
 
RUN chmod +x /runViessmann.sh /watchdog.sh /entrypoint.sh

ENTRYPOINT /entrypoint.sh