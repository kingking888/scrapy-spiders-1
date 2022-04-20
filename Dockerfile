# syntax = docker/dockerfile:1.2

FROM amd64/python:3.8.10-slim as base-builder


RUN apt update && \
  apt install --no-install-recommends -y curl && \
  curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3 && \
  ${HOME}/.poetry/bin/poetry config virtualenvs.create false

ENV PATH="root/.poetry/bin:${PATH}"

FROM base-builder AS builder

RUN apt install --no-install-recommends -y git

COPY . .
RUN --mount=type=cache,target=/root/.cache/pypoetry \
  poetry install --no-root

FROM amd64/python:3.8.10-slim AS base-runner

RUN apt-get update && \
   apt-get -y clean && \
   apt-get -y autoremove && \
   rm -rf /var/lib/apt/lists/*

FROM base-runner as runner

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/scrapy /usr/local/bin/scrapy

COPY src/ spiders/

WORKDIR /spiders
CMD ["scrapy", "list"]
