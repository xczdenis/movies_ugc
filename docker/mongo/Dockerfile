ARG IMG=mongo:latest
ARG ENV=production

FROM ${IMG} as builder

ARG ENV

COPY ./docker/scripts /scripts
RUN chmod -R 777 /scripts


FROM builder as development

EXPOSE 27017


FROM builder as production

COPY ./docker/mongo/scripts /scripts/init
RUN chmod -R 777 /scripts


FROM ${ENV}
