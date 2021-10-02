#!/bin/bash
source env/bin/activate
python3 manage.py db upgrade
service cron start
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app