FROM python:3.12-slim-bookworm

# Add non-root user
RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the project requirements.
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail . .

USER wagtail

WORKDIR /app/radioclub_site

# Collect static files at build time.
RUN DJANGO_SETTINGS_MODULE=radioclub_site.settings.production \
    SECRET_KEY=build-only-secret-key \
    python manage.py collectstatic --noinput --clear

# Migrate and start gunicorn.
CMD set -xe; \
    python manage.py migrate --noinput; \
    gunicorn radioclub_site.wsgi:application \
        --bind 0.0.0.0:${PORT} \
        --workers 3 \
        --timeout 120
