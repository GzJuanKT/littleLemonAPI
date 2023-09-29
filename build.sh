#!/usr/bin/env bash
# exit on error
set -o errexit

export PIPENV_DONT_LOAD_ENV=1
pipenv install --dev

python manage.py collectstatic --no-input
python manage.py migrate