#!/bin/sh
set -e

# clickhouse-zookeeper
echo "\033[94mWaiting the service: \033[97mclickhouse-zookeeper (url=$CH_ZOO_HOST_NAME:$CH_ZOO_PORT_NUMBER)\033[00m"
/scripts/wait-for-it.sh $CH_ZOO_HOST_NAME:$CH_ZOO_PORT_NUMBER -t 120 --
echo "\033[01;32mclickhouse-zookeeper is up!\033[00m"

exec "$@"
