#!/bin/bash
printenv | sed 's/^\(.*\)$/\1/g' > loaded.env
flask db upgrade
service cron start
crontab explinks-crontab
crontab -l >> loaded.env
crontab loaded.env
exec gunicorn -b :5000 --access-logfile - --error-logfile - --worker-class eventlet -w 1 manage:app