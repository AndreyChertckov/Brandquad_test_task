#!/bin/sh

echo "Migrations"
python manage.py makemigrations apache_log
python manage.py migrate

echo "Load apache log"
python manage.py load_log http://www.almhuette-raith.at/apache-log/access.log

echo "Start server"
python manage.py runserver 0.0.0.0:8000