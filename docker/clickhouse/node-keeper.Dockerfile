ARG IMG=clickhouse/clickhouse-server:latest
FROM ${IMG}

COPY ./docker/clickhouse/config /etc/clickhouse-server
COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
COPY ./docker/scripts /scripts

COPY ./docker/clickhouse/config/enable_keeper.xml /etc/clickhouse-server/config.d/enable_keeper.xml
