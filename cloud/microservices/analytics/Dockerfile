FROM python:3.11-slim-bookworm

RUN useradd -m -u 1000 analytics

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src

USER analytics
ENV PYTHONUNBUFFERED=1
EXPOSE 8095
CMD ["python", "src/main.py"]
