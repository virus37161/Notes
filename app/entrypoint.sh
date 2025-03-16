#!/bin/sh

if [ "$POSTGRES_DB" = "notes" ]
then
    echo "Ждем postgres..."

    while ! nc -z "db" $POSTGRES_PORT; do
      sleep 0.5
    done

    echo "PostgreSQL запущен"
fi

alembic upgrade head

exec "$@"