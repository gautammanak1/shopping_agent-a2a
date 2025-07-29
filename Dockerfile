FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "main.py"]

