#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi

#python manage.py makemigrations expplat
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"