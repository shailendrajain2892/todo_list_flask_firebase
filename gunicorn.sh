#!/bin/sh
gunicorn --bind 0.0.0.0:5000 --timeout 300 app:app
