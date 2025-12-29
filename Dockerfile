FROM python:3.12.8-slim AS dependencies_builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="/root/.local/bin:$PATH"
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv sync

FROM python:3.12.8-slim
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"

COPY --from=dependencies_builder /root/.local /root/.local
COPY --from=dependencies_builder /app/.venv /app/.venv

COPY . .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# size decreased from 2.86GB to 2.54GB