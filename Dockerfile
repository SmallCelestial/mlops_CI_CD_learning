FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
# Sync inference group to .venv
RUN uv sync --frozen --group inference --no-install-project --no-dev

# Runtime stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY . .

# Run the application
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["app.handler"]