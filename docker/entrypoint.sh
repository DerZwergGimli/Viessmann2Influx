#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

chmod +x /runViessmann.sh /watchdog.sh 

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/5 * * * * /runViessmann.sh 2>&1
* * * * * /watchdog.sh 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
crond -f