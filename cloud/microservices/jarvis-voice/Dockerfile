FROM python:3.11-slim-bookworm

# Security: non-root user
RUN useradd -m -u 1000 voice

WORKDIR /app

# System deps for Whisper (ffmpeg)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER voice

ENV PYTHONUNBUFFERED=1
EXPOSE 8082

CMD ["python", "src/main.py"]
