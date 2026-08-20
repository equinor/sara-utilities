FROM ghcr.io/astral-sh/uv:0.12.5@sha256:e85be844203885286c60ffad8a858d48afb6c5a5c237ca0e67f12e74b8f174b1 AS uv
FROM python:3.14-slim@sha256:ce40764625a4ff50df3548277632e7f96c4e77fe75fa848aae9885476e7df5a4

COPY --from=uv /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY main.py ./
COPY sara_utilities ./sara_utilities

ENV PATH="/app/.venv/bin:$PATH"

RUN useradd --create-home --uid 1000 --shell /bin/bash app \
    && chown -R app:app /app
USER app

CMD ["python", "main.py"]
