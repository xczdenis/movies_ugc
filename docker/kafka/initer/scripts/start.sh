#!/bin/sh
. ./.venv/bin/activate

python src/${PROJECT_PKG_NAME}/kafka_initer.py
