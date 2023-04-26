ARG env=production

FROM python:3.11-slim as base

ENV CONTAINER_HOME_DIR=app \
    HOST_SRC_DIR=src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

WORKDIR $CONTAINER_HOME_DIR

ARG env


FROM base as builder

COPY ./docker/scripts /scripts
COPY ./docker/app/scripts /scripts
RUN chmod -R 777 /scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && pip install poetry==$POETRY_VERSION \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main


FROM base as final
COPY --from=builder /scripts /scripts
COPY --from=builder /$CONTAINER_HOME_DIR/.venv ./.venv


FROM final as development


FROM final as production

COPY ./$HOST_SRC_DIR ./$HOST_SRC_DIR


FROM ${env}

ENTRYPOINT ["/scripts/entrypoint.sh"]
