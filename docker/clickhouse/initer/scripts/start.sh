#!/bin/sh
. ./.venv/bin/activate

python src/${PROJECT_PKG_NAME}/olap_db_initer.py
