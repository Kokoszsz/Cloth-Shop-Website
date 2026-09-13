# Stage one builds the dependency wheels, so the compiler and build tooling it
# needs never reach the image that ships.
FROM python:3.11-slim AS build

WORKDIR /build

COPY requirements.txt ./
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/Web \
    APP_ENV=production \
    DATABASE_URL=sqlite:////data/mydb.db \
    SEED_JSON=/app/Databases/json/data.json

COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# /data is the mount point for the database volume. Creating it here, owned by
# the application user, is what lets a fresh named volume inherit that
# ownership; without it the non-root process cannot open the database file.
RUN useradd --create-home --uid 1000 appuser \
    && mkdir /data \
    && chown appuser:appuser /data

WORKDIR /app
COPY --chown=appuser:appuser Web/ ./Web/
COPY --chown=appuser:appuser Databases/json/ ./Databases/json/
COPY --chown=appuser:appuser docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER appuser
WORKDIR /app/Web
EXPOSE 5000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", \
     "--access-logfile", "-", "main:create_app()"]
