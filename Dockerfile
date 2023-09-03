FROM python:3.11-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

FROM base AS python-deps

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev && rm -rf /var/lib/apt/lists/*

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home appuser
WORKDIR /src
USER appuser

COPY . /src/
