#!/bin/bash
source env/bin/activate
flask db upgrade
service cron start
crontab explinks-crontab
exec gunicorn -b :5000 --access-logfile - --error-logfile - --worker-class eventlet -w 1 manage:app