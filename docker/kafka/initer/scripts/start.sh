#!/bin/sh
. ./.venv/bin/activate

python src/${PROJECT_PKG_NAME}/oltp_db_initer.py
