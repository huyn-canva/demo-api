#!/bin/bash

export FLASK_APP=app.py
export FLASK_RUN_PORT=3001
export FLASK_RUN_HOST="127.0.0.1"

if [ -n "$1" ] && [ $1 = "debug" ]; then
    flask --debug run
else
    flask run
fi 