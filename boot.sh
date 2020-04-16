#!/bin/sh
source env/bin/activate
#flask db upgrade
flask translate compile
#exec gunicorn -b :5000 --access-logfile - --error-logfile - jbin:app
python3 manage.py runserver