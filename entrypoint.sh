#!/bin/sh

# Зупинити виконання скрипту при помилці
set -e

# Створення міграцій
python manage.py makemigrations

# Виконання міграцій
python manage.py migrate --noinput

# Запуск сервера Django
exec python manage.py runserver 0.0.0.0:8000
