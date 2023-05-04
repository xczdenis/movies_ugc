#!/bin/sh
set -e

. /scripts/colors.sh
. /scripts/logger.sh
. /scripts/helpers.sh


check_service "mongo-configsvr01" "mongo-configsvr01" "27017"

log_success "All services is up!"
echo ""

exec "$@"
