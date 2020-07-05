#!/usr/bin/env bash
touch /app/debug.log
chmod 777 /app/debug.log
service nginx start
uwsgi --ini uwsgi.ini