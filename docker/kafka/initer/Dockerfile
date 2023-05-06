FROM python-src

COPY ./docker/kafka/initer/scripts /scripts
RUN chmod -R 777 /scripts

ENTRYPOINT ["/scripts/entrypoint.sh"]
