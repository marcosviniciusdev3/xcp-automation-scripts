FROM python:3.13.15-alpine3.24

# Prevent Python from writing .pyc files and unbuffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /scripts

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY *.py .

ENTRYPOINT ["python"]
