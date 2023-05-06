#!/bin/sh
. ./.venv/bin/activate

python src/${PROJECT_PKG_NAME}/clickhouse_initer.py
