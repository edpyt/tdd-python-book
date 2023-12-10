#!/bin/bash

gunicorn superlists.wsgi:application \
        -b unix:/gunicorn_socket/tdd.pythonbook.com.socket \
        --access-logfile ../access.log \
        --error-logfil ../error.log
        