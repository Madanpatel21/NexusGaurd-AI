# Stage 1: Build
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache layer)
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /tmp/wheels -r requirements.txt

# Copy source code
COPY . .

# Stage 2: Run (Minimal Python image)
FROM python:3.11-slim-bookworm

# Security: Non-root user
RUN useradd -m -u 1000 nexusguard

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /tmp/wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/*

# Copy source code
COPY --from=builder /app/src ./src
COPY --from=builder /app/models ./models

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run as non-root
USER nexusguard

CMD ["python", "src/agent.py"]
