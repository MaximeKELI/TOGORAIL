# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for Pillow + psycopg + gettext (translations)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Collect static + compile translations at build time
ENV DJANGO_SETTINGS_MODULE=config.settings
RUN python manage.py collectstatic --noinput || true \
    && python manage.py compilemessages || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "-c", "gunicorn.conf.py"]
