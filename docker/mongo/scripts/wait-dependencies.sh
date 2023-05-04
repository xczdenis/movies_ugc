#!/bin/sh
set -e

. /scripts/colors.sh
. /scripts/logger.sh
. /scripts/helpers.sh


check_service "mongo-shard01-a" "mongo-shard01-a" "27017"
check_service "mongo-shard02-a" "mongo-shard02-a" "27017"
check_service "mongo-configsvr01" "mongo-configsvr01" "27017"

log_success "Mongo shards and config servers is up!"
echo ""

exec "$@"
