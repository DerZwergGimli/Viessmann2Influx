# Cretae a telegraf container containing python and later install own application
FROM alpine:latest
ENV TZ Europe/Berlin
#RUN apt-get update 
#RUN apt-get install -y --no-install-recommends apt-utils
#RUN apt-get upgrade -y && apt-get install -y python3 python3-pip cron nano

RUN apk update 
#RUN apk add --no-install-recommends apt-utils
RUN apk upgrade 
RUN apk add bash
RUN apk add python3 
RUN apk add py3-pip 
RUN apk add openrc
#RUN apk add cron nano
#RUN rc-service crond start && rc-update add crond

#Just some feedback about the version
RUN python3 -V
RUN pip3 -V
#RUN pip3 install --upgrade pip

# SETUP Viessmann2Influx
ADD ./app /home/app/Viessmann2Influx
RUN pip3 install --ignore-installed -r /home/app/Viessmann2Influx/requirements.txt



## The following steps are now done in the docker-compose - i leave this in for developement!
# Add files for cron
ADD ./docker/entrypoint.sh /entrypoint.sh
#ADD ./docker/runViessmann.sh /runViessmann.sh
#ADD ./docker/watchdog.sh /watchdog.sh

RUN chmod +x /entrypoint.sh
#RUN chmod +x /runViessmann.sh /watchdog.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]