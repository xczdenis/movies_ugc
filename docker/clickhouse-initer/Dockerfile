FROM python:3.10.0-slim as base

ENV HOME_DIR=app \
    PROJECT_PACKAGE=src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.2.2


FROM base as builder

WORKDIR /$HOME_DIR

COPY ./docker/scripts /scripts
COPY ./docker/clickhouse-initer/scripts /scripts
RUN chmod -R 777 /scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libpq-dev \
        build-essential \
    && pip install poetry==$POETRY_VERSION \
    && python -m venv /venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./
COPY ./$PROJECT_PACKAGE ./$PROJECT_PACKAGE
RUN poetry build && /venv/bin/pip install dist/*.whl


FROM base

COPY --from=builder /scripts /scripts
COPY --from=builder /venv /venv
COPY --from=builder /$HOME_DIR /$HOME_DIR

WORKDIR /$HOME_DIR/$PROJECT_PACKAGE

#ENTRYPOINT ["/scripts/entrypoint.sh"]
ENTRYPOINT ["/scripts/start.sh"]
