ARG CH_SERVER_IMG_VER
FROM yandex/clickhouse-server:${CH_SERVER_IMG_VER}

COPY ./docker/clickhouse/config /etc/clickhouse-server
COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
COPY ./docker/scripts /scripts

COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
