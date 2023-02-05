#!/bin/sh

gunicorn --bind 0.0.0.0:5000 --log-config log.conf 'run:create_app()'