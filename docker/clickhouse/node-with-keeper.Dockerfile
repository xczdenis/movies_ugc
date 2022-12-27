#ARG CH_SERVER_IMG_VER
#FROM yandex/clickhouse-server:${CH_SERVER_IMG_VER}
#
#COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
#COPY ./docker/clickhouse/config1 /etc/clickhouse-server/config.d
#COPY ./docker/scripts /scripts




#ARG CH_SERVER_IMG_VER
#FROM yandex/clickhouse-server:${CH_SERVER_IMG_VER}
#
#COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
#COPY ./docker/clickhouse/_config/config.d /etc/clickhouse-server/config.d
#COPY ./docker/clickhouse/_config/enable_keeper.xml /etc/clickhouse-server/config.d/enable_keeper.xml
#COPY ./docker/clickhouse/_config/metrika.xml /etc/metrika.xml
#COPY ./docker/scripts /scripts




#ARG CH_SERVER_IMG_VER
#FROM yandex/clickhouse-server:${CH_SERVER_IMG_VER}
#
#COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
#COPY ./docker/clickhouse/config/config.d /etc/clickhouse-server/config.d
##COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
#COPY ./docker/clickhouse/config/enable_keeper.xml /etc/clickhouse-server/config.d/enable_keeper.xml
#COPY ./docker/scripts /scripts

ARG CH_SERVER_IMG_VER
FROM yandex/clickhouse-server:${CH_SERVER_IMG_VER}

COPY ./docker/clickhouse/initdb /docker-entrypoint-initdb.d
COPY ./docker/clickhouse/config /etc/clickhouse-server
COPY ./docker/clickhouse/config/metrika.xml /etc/metrika.xml
COPY ./docker/clickhouse/config/enable_keeper.xml /etc/clickhouse-server/config.d/enable_keeper.xml
COPY ./docker/scripts /scripts
