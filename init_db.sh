#!/bin/bash
set -e
# Завантажити змінні з .env
export $(grep -v '^#' .env | xargs)

# Запуск лише бази
docker compose up -d db

# Чекати готовності
echo "Waiting for Postgres to be ready..."
until docker compose exec -T db pg_isready -U $POSTGRES_USER > /dev/null 2>&1; do
    sleep 1
done
echo "Database ready!"

# Ініціалізація
docker compose run --rm app python3 -m src.seed_database
echo "Database initialized!"

# Перезапуск сервісів
docker compose restart
