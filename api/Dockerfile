FROM python:3.11-slim-bullseye as base

USER root
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev wait-for-it \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

RUN python -m pip install --upgrade pip

COPY api/ .

RUN pip install -r requirements.txt


FROM base as dev
RUN pip install -r dev-requirements.txt