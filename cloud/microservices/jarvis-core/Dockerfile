FROM python:3.11-slim-bookworm

# Security: non-root user
RUN useradd -m -u 1000 jarvis

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY .env.example .env

USER jarvis

ENV PYTHONUNBUFFERED=1
EXPOSE 8081

CMD ["python", "src/main.py"]
