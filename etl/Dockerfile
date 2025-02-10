FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
COPY database.py .
COPY etl/pipeline.py .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install owslib

CMD ["python", "./pipeline.py"]