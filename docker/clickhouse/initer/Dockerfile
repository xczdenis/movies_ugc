FROM python-src

COPY ./docker/clickhouse/initer/scripts /scripts
RUN chmod -R 777 /scripts

ENTRYPOINT ["/scripts/entrypoint.sh"]
