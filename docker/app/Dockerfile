FROM python-src

COPY ./docker/app/scripts /scripts
RUN chmod -R 777 /scripts

ENTRYPOINT ["/scripts/entrypoint.sh"]
