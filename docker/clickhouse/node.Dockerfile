ARG CH_SERVER_IMG
FROM ${CH_SERVER_IMG}

COPY ./docker/clickhouse/config /etc/clickhouse-server
COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
COPY ./docker/scripts /scripts
