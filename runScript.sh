#!/bin/bash

port=8000;
host="$(hostname -I):$port";

echo "Starting server";
python3 manage.py runserver "${host//[[:blank:]]/}";
echo "Server Stopped";
