# --- Build stage: compilers and headers, only to build the Python packages (mysqlclient needs them) ---
FROM python:3.14-slim AS build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# --- Runtime stage: no compilers, no cron, runs as an unprivileged user ---
FROM python:3.14-slim

# libmariadb3 is the client library mysqlclient links against at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmariadb3 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home --home-dir /nonexistent --shell /usr/sbin/nologin app

ENV PATH=/opt/venv/bin:$PATH \
    FLASK_APP=manage.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=build /opt/venv /opt/venv

# The code stays owned by root and read-only for the app user, so a compromised process can't rewrite it.
WORKDIR /app
COPY app app
COPY migrations migrations
COPY manage.py config.py boot.sh .flaskenv ./
RUN chmod 755 boot.sh

# Numeric, so Kubernetes `runAsNonRoot` can verify it.
USER 10001

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
