#!/bin/sh
set -e

DATABASE_FILE=${DATABASE_FILE:-/data/mydb.db}

if [ ! -f "$DATABASE_FILE" ]; then
    echo "No database at $DATABASE_FILE, seeding a new one."
    python /app/Web/create_database.py
fi

exec "$@"
