FROM yandex/clickhouse-server:21.3

COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
COPY ./docker/clickhouse/config /etc/clickhouse-server
COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
