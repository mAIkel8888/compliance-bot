# Stage 1: Base Image
FROM python:3.11-slim AS base

# Set environment variables to ensure the Python app runs reliably
#   PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files.
#   PYTHONUNBUFFERED=1: Ensures logs are output immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Builder Image (for dependencies)
FROM base AS builder

# Install virtualenv
RUN python -m pip install --upgrade pip && pip install virtualenv

# Create a virtual environment
WORKDIR /app
RUN virtualenv .venv

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 3: Final Image
FROM base AS final

# Set working directory
WORKDIR /app

# Copy application code
COPY source/ .

# Copy virtual environment from the builder stage
COPY --from=builder /app/.venv .venv

# Expose port (adjust if your app uses a specific port)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application using the virtual environment
ENTRYPOINT ["streamlit", "run"]
CMD [ "/app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]