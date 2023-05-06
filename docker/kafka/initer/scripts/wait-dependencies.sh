#!/bin/sh
set -e

. /scripts/colors.sh
. /scripts/logger.sh
. /scripts/helpers.sh


check_service "Kafka-broker" "${KAFKA_CONNECTION_HOST}" "${KAFKA_CONNECTION_PORT}"
check_service "Kafka-schema-registry" "${KAFKA_SCHEMA_REGISTRY_HOST}" "${KAFKA_SCHEMA_REGISTRY_PORT}"

log_success "All services is up!"
echo ""

exec "$@"
