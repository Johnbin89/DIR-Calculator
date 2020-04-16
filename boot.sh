#!/bin/sh
source env/bin/activate
exec python3 manage.py runserver --host 0.0.0.0