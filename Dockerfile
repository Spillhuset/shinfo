# base image
FROM python:3.12.4-alpine@sha256:d24ed567ee3b972478a232ceff84b0d002e18ee9f5d38234ecbffece23dfa084 AS base
WORKDIR /app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# dependencies
FROM node:18-alpine@sha256:1b32fb34435dc694e244b84fcfdf2642b004014170462d69c5c3ac9833617754 AS node
FROM base AS builder

## poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN mkdir docs && touch README.md

RUN --mount=type=cache,target=${POETRY_CACHE_DIR} poetry install --only=main
ENV PATH="/app/.venv/bin:$PATH"

# tailwind needs node 💀
COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local/share /usr/local/share
COPY --from=node /usr/local/lib /usr/local/lib
COPY --from=node /usr/local/include /usr/local/include
COPY --from=node /usr/local/bin /usr/local/bin

COPY ./src ./src
WORKDIR /app/src

RUN SECRET_KEY=dummy \
    python3 manage.py tailwind install && \
    python3 manage.py tailwind build && \
    python3 manage.py collectstatic --noinput

# runtime nginx image
FROM nginx:alpine@sha256:1e67a3c8607fe555f47dc8a72f25424b10273639136c061c508628da3112f90e AS runtime-nginx

COPY --from=builder /app/src/static_built /var/www/html/static
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# runtime image
FROM base AS runtime

ENV DB_ENGINE=postgresql

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY ./src ./src
COPY --from=builder /app/src/static_built/staticfiles*.json /app/src/static_built/

WORKDIR /app/src
EXPOSE 80
