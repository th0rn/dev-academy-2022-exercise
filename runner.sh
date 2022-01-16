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

# Ask whether to (re-)import data from CSV files or not. If we'd deploy this, this would
# have to be handled another way, like with a flag.
echo -n "Import data from CSV-files? [Y/n]? "
read -r answer
if [[ ${answer} != "${answer#[Nn]}" ]]; then
    import=0
else
    import=1
fi

if ! cd app; then
    echo 'Fatal: app directory missing or inaccessible.'
    exit 1
fi

if ((import==1)); then
    # --run-syncdb to prevent errors caused by missing database tables when importing views.
    python manage.py migrate --run-syncdb
    python manage.py loaddata fixtures/farm_info.yaml
    python manage.py shell <<< 'import core.importer; core.importer.import_all()'
fi

python manage.py runserver
