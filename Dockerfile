FROM python:3.9-slim

WORKDIR /app

# Kopierar både app.py och requirements.txt
COPY requirements.txt .
COPY app.py .

# Create directory for SQLite database
RUN mkdir -p /data

# Installera sqlite3 CLI
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Installera Python-paket från requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]