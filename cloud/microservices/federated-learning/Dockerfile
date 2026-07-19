FROM python:3.11-slim-bookworm

# Security: Non-root user
RUN useradd -m -u 1000 nexusguard

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run as non-root
USER nexusguard

CMD ["python", "src/orchestrator.py"]
