FROM python-src

COPY ./docker/mongo/initer/scripts /scripts
RUN chmod -R 777 /scripts

ENTRYPOINT ["/scripts/entrypoint.sh"]
