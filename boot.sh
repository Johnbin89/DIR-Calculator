#!/bin/bash
printenv | sed 's/^\(.*\)$/\1/g' > loaded.env
flask db upgrade
service cron start
crontab explinks-crontab
crontab -l >> loaded.env
crontab loaded.env
exec gunicorn -b :5000 --access-logfile - --error-logfile - --worker-class gthread -w 1 --threads 50 manage:app