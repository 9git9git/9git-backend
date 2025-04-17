# Use Python 3.12 slim image
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==2.1.1

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-root --no-interaction

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Set build time argument
ARG BUILD_DATE
ENV BUILD_DATE=$BUILD_DATE

# Expose port
EXPOSE 8000

# Command to run the application with --reload option for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 