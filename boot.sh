#!/bin/bash
set -e

flask db upgrade

# The daily cleanup of expired shared links (`flask delete_shared`) runs as a separate
# Kubernetes CronJob (k8s/cronjob.yaml), not from cron inside this container.
# --no-control-socket: gunicorn's local admin socket isn't used, and the read-only container has nowhere to put it.
exec gunicorn -b :5000 --access-logfile - --error-logfile - --no-control-socket --worker-class gthread -w 1 --threads 50 manage:app
