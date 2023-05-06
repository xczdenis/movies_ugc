FROM python-src

COPY ./docker/tests/scripts /scripts
RUN chmod -R 777 /scripts

COPY ./tests /app/tests

ENTRYPOINT ["/scripts/entrypoint.sh"]
