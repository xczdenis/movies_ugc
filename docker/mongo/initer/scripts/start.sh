#!/bin/sh
. ./.venv/bin/activate

python src/${PROJECT_PKG_NAME}/mongo_db_initer.py
