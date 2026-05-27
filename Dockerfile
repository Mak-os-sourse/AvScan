FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install uv
RUN uv sync
RUN uv run playwright install --with-deps chromium