#!/usr/bin/env bash
touch /app/debug.log
chmod 777 /app/debug.log
uwsgi --ini uwsgi.ini