#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install --dev
pipenv shell

python manage.py collectstatic --no-input
python manage.py migrate