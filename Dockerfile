# Multi-stage build for production runtime
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final runtime image
FROM python:3.13-slim AS runner

WORKDIR /app

# Copy installed site-packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code and docs
COPY src/ ./src/
COPY docs/openapi.yaml ./docs/openapi.yaml

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose microservice port
EXPOSE 8000

# Run FastAPI app via Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
