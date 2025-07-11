FROM python:3-alpine

# Install poetry
RUN pip install poetry

WORKDIR /app

# Copy poetry files first (for better Docker layer caching)
COPY pyproject.toml poetry.lock* ./

# Copy application code (this layer changes more frequently)
COPY . .

# Install dependencies (this layer will be cached if dependencies don't change)
RUN poetry install --only=main

# Expose port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]