#!/bin/bash
# The runner to serve our django app.

py_VERSION='Python 3.10.1'

if [[ ! -d app/farms ]]; then
    echo "Run me from project root: cd <project_root> && ./runner.sh"
    exit 1
fi

if ! command -v python >/dev/null; then
    echo 'You must have python installed and in $PATH to run this.'
    exit 1
fi

version="$(python --version)"
if [[ ${version} != "${py_VERSION}" ]]; then
    echo "This app has been tested on ${py_VERSION}, but you are running ${version}."
    echo "Your mileage may or may not vary."
fi

if [[ ! -d env ]]; then
    python -m venv env
fi
source env/bin/activate
pip install -r requirements.txt

# When running interactively, ask whether to (re-)import data from CSV files or not.
if [[ $- == *i* ]]; then
    # TODO: this.
    true
else
    # import=1
    true
fi
import=1

if ((import==1)); then
    if ! cd app; then
        echo 'Fatal: app directory missing or inaccessible.'
        exit 1
    fi
    python manage.py shell <<< 'import core.importer; core.importer.import_all()'
fi

python manage.py runserver
