# Cloth Shop — a Flask shop, its API, and the tests around it

[![Tests](https://github.com/Kokoszsz/Cloth-Shop-Website/actions/workflows/test.yml/badge.svg)](https://github.com/Kokoszsz/Cloth-Shop-Website/actions/workflows/test.yml)
![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)

An e-commerce site built with Flask — catalogue, filtering, ratings, reviews,
basket and checkout — together with a documented JSON API, a container image,
and four layers of tests running in CI.

The repository holds the shop and the test work around it, because the two were
built together: the manual test cases and the bug reports came first, and the
automated suites grew out of them.

```bash
git clone https://github.com/Kokoszsz/Cloth-Shop-Website.git
cd Cloth-Shop-Website/cloth-shop
cp .env.example .env          # then put a value in SECRET_KEY
docker compose up --build     # http://localhost:5000
```

## Start here

If you are reading the code rather than running it, these are the files worth the
first few minutes:

| File | Why |
| --- | --- |
| [`Web/config.py`](cloth-shop/Web/config.py) | One settings class per environment; production refuses to boot without a `SECRET_KEY` rather than inventing one |
| [`Web/main.py`](cloth-shop/Web/main.py) | The application factory and how the four blueprints are wired together |
| [`Web/blueprints/api.py`](cloth-shop/Web/blueprints/api.py) | The `/api/v1` endpoints — schema-validated, self-documenting, one error shape throughout |
| [`Web/models.py`](cloth-shop/Web/models.py) | Password hashing, unique constraints and value validation at the model |
| [`Web/database.py`](cloth-shop/Web/database.py) | `session_scope`: one place that commits, rolls back and closes |
| [`Dockerfile`](cloth-shop/Dockerfile) | Two-stage build, gunicorn, non-root user |

The [security](cloth-shop/README.md#security) and
[testing](cloth-shop/README.md#testing) sections of the project README explain
the decisions behind those, including the ones where something was removed
instead of added.

## What is in here

### [Cloth Shop Website](./cloth-shop)

The Flask application: app factory, four blueprints, SQLAlchemy models, the
`/api/v1` JSON API with Swagger UI at `/api/docs`, and a Dockerfile with compose.

### [Python automation tests](./automation-tests)

Selenium suites covering login, logout, filters and basket flows in Firefox, plus
a Playwright journey that runs in CI on every push.

### [Manual tests](./manual-tests)

Test cases written and executed in Jira, exported to CSV — the exploratory work
the automated suites were built from.
